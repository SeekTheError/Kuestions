from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import  render_to_response
from couchdbinterface.dblayer import view,getDocument
from model.entities import Question

from security.userauth import checkSession,getCurrentUser

#retrival of the couchdb credentials
file = open('.couchDbCredentials','r')
creds=file.readline().replace('\n','').split(':')
credentials = creds[0]+':'+creds[1]


def post(request) :
  content=request.POST["question"]
  context=checkSession(request)
  user=getCurrentUser(context)
  print user.id
  if content != "": 
    q=Question(asker=user.login,content=content)
    q.create()
    context["message"]='question successfully posted'
  else :
    context["message"]='a question need words!'
  #remove the displayed question 
  context["question"]=None 
  context["questionSearchResults"]=None
  return render_to_response('index.html', context ,context_instance=RequestContext(request))
  
import urllib
def search(request) :
  '''
  mockup method to test the search function, soon to be implemented in javascript
  '''
  context=checkSession(request)
  searchTerms=request.GET["search"].encode('UTF8')
  url='http://'+credentials+'@localhost:5984/'+'kuestionsdb/_fti/_design/question/by_content?q='+searchTerms
  results=tempApiRedirect(url)
  questionSearchResults={}
  #remove the displayed question
  context["question"]=None
  context["message"]=''
  if results.has_key("rows") :    
    for row in  results["rows"]:
      doc = getDocument(row["id"])
      questionSearchResults[doc["_id"]]=doc["content"]  
    context["questionSearchResults"]=questionSearchResults
  return render_to_response('index.html', context ,context_instance=RequestContext(request))



def displayQuestion(request,question):
  context=checkSession(request)
  url='http://'+credentials+'@localhost:5984/'+'kuestionsdb/'+question
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
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
