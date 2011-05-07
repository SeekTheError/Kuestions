from django.http import HttpResponse
from model.entities import Question
from django.utils.encoding import smart_unicode
from security.userauth import checkSession,getCurrentUser
import json

#retrival of the couchdb credentials
file = open('.couchDbCredentials','r')
creds=file.readline().replace('\n','').split(':')
credentials = creds[0]+':'+creds[1]


def post(request) :
  content=smart_unicode(request.POST["question"], encoding='utf-8', strings_only=False, errors='strict')
  context=checkSession(request)
  user=getCurrentUser(context)
  if content != "": 
    q=Question(asker=user.login,content=content)
    print q
    q.create()
    message='question successfully posted'
  else :
<<<<<<< HEAD
    message='a question needs words!'
  #remove the displayed question 
  response = HttpResponse();
  response["message"]=message;
  return response;


def displayQuestion(request,question):
  context=checkSession(request)
  url='http://localhost:5984/kuestionsdb/'+question
  question=tempApiRedirect(url)
  context["question"]=question
  return render_to_response('index.html', context ,context_instance=RequestContext(request))
   
def tempApiRedirect(url):
  '''
  this function aim to allow us to query ressources from the django server in an api style
  keep in mind that this will leave, turn into a direct javascript query
  '''
  f= urllib.urlopen(url)
  jsonObject=''
  for line in f.readlines() :
      jsonObject+=line.replace('\n','')
  import json
  results=json.loads(jsonObject)
  return results
    message='a question need words!'
  return HttpResponse(message);

  
def viewQuestion(request):
  #obtain question by ID
  questionId = request.POST["questionId"]
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
  ratingType = request.POST["type"]
  answerId = request.POST["answerId"]
  questionId = request.POST["questionId"]


  q = Question(id=questionId)
  q = q.findById()

  updated = False
  for answer in q.answers:
    if answer.id == answerId:
      if ratingType == 'increment':
        answer.score += 1
      else:
        answer.score -= 1
      q.update()
      updated = True

  message = ''
  if updated:
    message = 'updated rating'
  else:
    message = 'could not update rating'

  #unwrap answer dictionaries so that we can serialize into json
  answerList = []
  for answer in q.answers:
    answerList.append(answer.unwrap())

  response = HttpResponse(json.dumps(answerList))
  response['message'] = message
  return response
