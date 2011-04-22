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
  q=Question(asker=user.id,content=content)
  q.create()
  context["message"]='question successfully posted'
  return render_to_response('index.html', context ,context_instance=RequestContext(request))
  
import urllib
def search(request) :
  '''
  mockup method to test the search function, soon to be implemented in javascript
  '''
  context=checkSession(request)
  searchTerms=request.GET["search"].encode('UTF8')
  url='http://'+credentials+'@localhost:5984/'+'kuestionsdb/_fti/_design/question/by_content?q='+searchTerms
  f= urllib.urlopen(url)
  jsonObject=''
  for line in f.readlines() :
      jsonObject+=line.replace('\n','')
      
  import json
  jsonObjects=json.loads(jsonObject)
  questionSearchResults={}
  for row in  jsonObjects["rows"]:
    doc = getDocument(row["id"])
    questionSearchResults[doc["_id"]]=doc["content"]  
  print questionSearchResults
  context["questionSearchResults"]=questionSearchResults
  return render_to_response('index.html', context ,context_instance=RequestContext(request))


def displayQuestion(request,question):
  print question
   