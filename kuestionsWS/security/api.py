from django.http import HttpResponse,Http404
import urllib
import couchdbinterface.couchdblayer as couchVar


KUESTIONS_API_GET_URL='/kuestions/api/get'

def gate(request) :
  #post method is not tested yet, and forbiden at the moment!'
  if request.POST :
    keeper(request)
    
  url=couchVar.SERVER_URL + request.path.replace(KUESTIONS_API_GET_URL,couchVar.DB_NAME)
  print 'new url: ',url
  f = urllib.urlopen(url)
  if f is not None :
    json=''
    for line in f.readlines() :
      json+=line.replace('\n','')
    return HttpResponse(removeProtectedFields(json))
  else :
    print 'api: error at the gate'
    keeper()

    

def removeProtectedFields(json) : 
  for field in privateFields :
    #"reString=',"('+field+')":(("[0-9A-Za-z\-@\.]+")|(null)|(true)|(false))'
    json=fieldRe.sub('',json)
  return json
#pre compile the regexp
import re
privateFields=['_rev','sessionId','password','session_expire','email','activationCode','isActivated']
expr=''
i=0
for field in privateFields:
  expr+='('+field+')'
  if not i > len(privateFields) - 2 :
    expr+='|'
  i+=1
reString=',"('+expr+')":(("[0-9A-Za-z\-@\.]+")|(null)|(true)|(false))'
fieldRe=re.compile(reString)

def keeper(request):
  raise Http404
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
