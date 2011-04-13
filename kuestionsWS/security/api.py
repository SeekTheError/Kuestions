from django.http import HttpResponse,Http404
import urllib
import couchdbinterface.couchdblayer as couchVar


KUESTIONS_API_GET_URL='/kuestions/api/get'

#TODO : modify the url scheme for the api
def gate(request) :
  '''
  this method play the role of a security proxy, by only allowing GET method directly to couchdb,
  and then filtering the resulting json to remove some parameter that should remain server side
  '''
  if request.POST :
    keeper(request,'Invalid Acces, use of a POST method')
    
  url=couchVar.SERVER_URL + request.path.replace(KUESTIONS_API_GET_URL,couchVar.DB_NAME)
  print 'new url: ',url
  if request.GET.__contains__('key') :
    param='?key=' + request.GET['key']
    url+=param
  
  f = urllib.urlopen(url)
  if f is not None :
    json=''
    for line in f.readlines() :
      json+=line.replace('\n','')
    return HttpResponse(removeProtectedFields(json))
  else :
    keeper(request,'error at the gate')

def removeProtectedFields(json) : 
  for field in privateFields :
    json=fieldRe.sub('',json)
  return json



#pre compile the regexp for the removeProtectFields function
import re
privateFields=['_rev','sessionId','password','sessionExpire','email','activationCode','isActivated']
expr=''
i=0
for field in privateFields:
  expr+='('+field+')'
  if not i > len(privateFields) - 2 :
    expr+='|'
  i+=1
reString=',"('+expr+')":(("[0-9A-Za-z\-@\.]+")|(null)|(true)|(false))'
fieldRe=re.compile(reString)

def keeper(request,message=''):
  print 'WARNING, api: '+message
  raise Http404
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
