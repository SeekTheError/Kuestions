from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import  render_to_response
from model.entities import Question
from django.utils.encoding import smart_unicode
from security.userauth import checkSession,getCurrentUser

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
    message='a question need words!'
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
  
def viewQuestion(request):
  #obtain question by ID
  questionId = request.POST["questionId"]
  q = Question(id=questionId)
  q = q.findById()

  #q.answers is not serializable... need to translate to dict
  answerList = [] 
  for answer in q.answers:
    answerDict = {
      'content': answer.content,
      'poster': answer.poster,
      'score': answer.score,
    }
    answerList.append(answerDict)


  import json
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

  print q

  answer = {'content': request.POST["answer"]}
  q.answers.append(answer)
  q.update()
  print 'answer added to question: ' + str(q)

  return HttpResponse(answer['content'])

