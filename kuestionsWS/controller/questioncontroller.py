from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import  render_to_response
from model.entities import Question
from django.utils.encoding import smart_unicode
from security.userauth import checkSession, getCurrentUser
import json

#retrival of the couchdb credentials
file = open('.couchDbCredentials', 'r')
creds = file.readline().replace('\n', '').split(':')
credentials = creds[0] + ':' + creds[1]


def post(request) :
  questionContent = smart_unicode(request.POST["question"], encoding='utf-8', strings_only=False, errors='strict')
  tags=smart_unicode(request.POST["tags"], encoding='utf-8', strings_only=False, errors='strict')
  topics=tags.split(',')
  print topics
  context = checkSession(request)
  user = getCurrentUser(context)
  if questionContent != "": 
    q = Question(asker=user.login, content=questionContent,topics=topics)

    print q
    q.create()
    message = 'question successfully posted'
  else :
    message = 'a question needs words!'
  #remove the displayed question 
  response = HttpResponse();
  response["message"] = message;
  return response;

   
def tempApiRedirect(url):
  '''
  this function aim to allow us to query ressources from the django server in an api style
  keep in mind that this will leave, turn into a direct javascript query
  '''
  f = urllib.urlopen(url)
  jsonObject = ''
  for line in f.readlines() :
      jsonObject += line.replace('\n', '')
  import json
  results = json.loads(jsonObject)
  return results
  
def viewQuestion(request):
  #obtain question by ID
  questionId = request.POST["questionId"]
  q = Question(id=questionId)
  q = q.findById()
  if q.views is None:
    q.views=0
  q.views=q.views+1
  q.update()
  #q.answers is not serializable... need to translate to dict
  
  
  answerList = [] 
  for answer in q.answers:
    answerDict = {
      'content': answer.content,
      'poster': answer.poster,
      'score': answer.score,
    }
    answerList.append(answerDict)


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
  context = checkSession(request)
  currentUser = getCurrentUser(context)
  if currentUser:
    #retrieve question
    questionId = request.POST["questionId"]
    q = Question(id=questionId)
    q = q.findById()
    
    #generate answer
    answer = {'content': request.POST["answer"]}
    answer['poster'] = currentUser.login
    answer['score'] = 0
    q.answers.append(answer)
    q.update()
    print 'answer added to question: ' + str(q)
    context = {}
    context['success'] = True
    context['answer'] = answer['content']
    return HttpResponse(json.dumps(context))
  else :
    context = {}
    context['success'] = False
    context['message'] = 'You need to be logged in to post an Answer'
    return HttpResponse(json.dumps(context))
