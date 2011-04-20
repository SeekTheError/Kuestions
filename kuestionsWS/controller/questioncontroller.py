from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import  render_to_response
from couchdbinterface.dblayer import view,getDocument

from security.userauth import checkSession

def post(request) :
  pass
 
 
import urllib
def search(request) :
  '''
  mockup method to test the search
  '''
  context=checkSession(request)
  searchTerms=request.GET["search"].encode('UTF8')
  f= urllib.urlopen('http://django:azer1234azer@localhost:5984/'+
                    'kuestionsdb/_fti/_design/question/by_content?q='+searchTerms)
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
   