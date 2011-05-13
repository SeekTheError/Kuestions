from django.http import HttpResponse
from model.entities import Question,Rating,TimeLineEvent
from django.utils.encoding import smart_unicode
from security.userauth import checkSession, getCurrentUser
import json
from hashlib import sha1

#retrival of the couchdb credentials
file = open('.couchDbCredentials', 'r')
creds = file.readline().replace('\n', '').split(':')
credentials = creds[0] + ':' + creds[1]


def post(request) :
  questionContent = smart_unicode(request.POST["question"], encoding='utf-8', strings_only=False, errors='strict')
  context = checkSession(request)
  user = getCurrentUser(context)
  if questionContent != "" and user: 
    q = Question(asker=user.login, content=questionContent)
    if request.POST.__contains__("tags") :
      tags=smart_unicode(request.POST["tags"], encoding='utf-8', strings_only=False, errors='strict')
      topics=tags.split(',')
      q.topics=topics
    print q
    q.create()
    q=q.findById()
    user=user.findByLogin()
    user.followedQuestions.append(q.id);
    user.update()
    message = 'question successfully posted'
  else :
    message = 'a question needs words!'
  #remove the displayed question 
  response = HttpResponse();
  response["message"] = message;
  return response;
  
def viewQuestion(request):
  #obtain question by ID
  questionId = request.GET["questionId"]
  q = Question(id=questionId)
  q = q.findById()
  if q.views is None :
    q.views = 0
  q.views+=1
  q.update()
  
  #unwrap answer dictionaries so that we can serialize into json
  answerList = []
  for answer in q.answers:
    answerList.append(answer.unwrap())

  response = json.dumps({
    'id': q.id,
    'content': q.content,
    'asker': q.asker,
    'views': q.views,
    'answers': answerList,
  })
  return HttpResponse(response)

def postAnswer(request):
  #obtain question by ID
  questionId = request.POST["questionId"]
  q = Question(id=questionId)
  q = q.findById()

  #create answer ID by hashing (userId, questionId) 
  context=checkSession(request)
  user = getCurrentUser(context)
  if user is None:
    return HttpResponse(json.dumps({'error':1, 'errorMessage': 'You need to be logged in to post an answer'}))
  answerId = sha1(user.id + questionId).hexdigest()

  #check if answer ID already exists
  #this means that this user already posted an answer for this question -> abort post
  #the following is deactivated for development purposes
  '''
  for answer in q.answers:
    if answer.id == answerId:
      return HttpResponse(json.dumps({'error':1, 'errorMessage': 'You have already posted an answer for this Kuestion!'}))
  '''
  content = request.POST["answer"]
  newAnswer = {'content': content, 'id': answerId, 'poster':user.login }
  q.answers.append(newAnswer)
  q.update()
  #time line event creation
  t=TimeLineEvent()
  t.user=user.login
  t.action="POST"
  t.questionTitle=Question(id=questionId).findById().content
  t.answer=answerId
  t.question=questionId
  t.create()

  print t
  
  
  print 'answer added to question: ' + str(q)

  #unwrap answer dictionaries so that we can serialize into json
  answerList = []
  for answer in q.answers:
    answerList.append(answer.unwrap())

  return HttpResponse(json.dumps(answerList))

def rateAnswer(request):
  context=checkSession(request)
  user = getCurrentUser(context)
  questionId = request.POST["questionId"]
  
  if user is None:
    response=HttpResponse(getAnswersJson(questionId))
    response['message']='You must be logged in to rate an answer'
    return response
    
  
  ratingType = request.POST["type"]
  answerId = request.POST["answerId"]
  
  r=Rating(_id=sha1(user.id+answerId).hexdigest())  
  if r.findById() :
    response=HttpResponse(getAnswersJson(questionId))
    response['message']='You have already rate this answer'
    return response
  
  
  q = Question(id=questionId)
  q = q.findById()
  updated = False
  for answer in q.answers:
    if answer.id == answerId:
      if answer.score is None:
        answer.score =0
      if ratingType == 'increment':
        answer.score += 1
      else:
        answer.score -= 1
      q.update()
      updated = True

  message = ''
  if updated:
    message = 'updated rating'
    r.create();
  else:
    message = 'could not update rating'

  #unwrap answer dictionaries so that we can serialize into json
  answerList = []
  for answer in q.answers:
    answerList.append(answer.unwrap())
  response = HttpResponse(json.dumps(answerList))
  response['message'] = message
  return response

def getAnswersJson(questionId):
  q = Question(id=questionId)
  q = q.findById()
  answerList = []
  for answer in q.answers:
    answerList.append(answer.unwrap())
  return json.dumps(answerList)

def manageFollowQuestion(request):
  '''
  post has two parameter : 
  the question Id
  and an action, fo(follow) or un(unfollow)
  '''
  context=checkSession(request)
  user = getCurrentUser(context)
  if user is None:
    response=HttpResponse()
    return response
  questionId=request.POST["questionId"]
  action=request.POST["action"]
  user=user.findByLogin()
  print 'action: '+action
  if action == 'fo' :
    contain=True
    try :
      user.followedQuestions.index(questionId)
    except ValueError :
      contain=False
    if not contain :    
      print 'appending question '+questionId
      user.followedQuestions.append(questionId)
      user.update()
    return HttpResponse(json.dumps({'followed':True}))                     
  if action == 'un':    
    try :
      user.followedQuestions.remove(questionId)
      user.update()
    except ValueError :
      pass
    return HttpResponse(json.dumps({'followed':False}))
  
def displayFollowedQuestions(request):
  context = checkSession(request)
  user = getCurrentUser(context)
  if user is None:
    return HttpResponse()

  user = user.findByLogin()

  questionList = []
  for questionId in user.followedQuestions:
    q = Question(id=questionId)
    q = q.findById()
    questionList.append({
      'id': q.id,
      'content': q.content,
    })

  return HttpResponse(json.dumps(questionList))
