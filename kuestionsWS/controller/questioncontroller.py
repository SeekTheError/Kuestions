from django.http import HttpResponse
from model.entities import Question,Rating
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
  from hashlib import sha1
  answerId = sha1(user.id + questionId).hexdigest()

  #check if answer ID already exists
  #this means that this user already posted an answer for this question -> abort post
  for answer in q.answers:
    if answer.id == answerId:
      return HttpResponse(json.dumps({'error':1, 'errorMessage': 'You have already posted an answer for this Kuestion!'}))

  content = request.POST["answer"]
  newAnswer = {'content': content, 'id': answerId }
  q.answers.append(newAnswer)
  q.update()
  print 'answer added to question: ' + str(q)

  #unwrap answer dictionaries so that we can serialize into json
  answerList = []
  for answer in q.answers:
    answerList.append(answer.unwrap())

  return HttpResponse(json.dumps(answerList))

def rateAnswer(request):
  context=checkSession(request)
  user = getCurrentUser(context)
  
  if user is None:
    response=HttpResponse(getAnswersJson(questionId))
    response['message']='You must be logged in to rate an answer'
    return response
    
  
  ratingType = request.POST["type"]
  answerId = request.POST["answerId"]
  questionId = request.POST["questionId"]
  
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
  
