from django.http import HttpResponse,Http404
import urllib
import couchdbinterface.couchdblayer as couchVar


KUESTIONS_API_GET_URL='/kuestions/api/get'

def gate(request) :
  print 'entering'
  #print '\nrequest data\n', request
  url=couchVar.SERVER_URL + request.path.replace(KUESTIONS_API_GET_URL,couchVar.DB_NAME)
  print 'new url: ',url
  f=None
  # POST not tested
  print 'warning, post method is not tested yet, and forbiden at the moment!'
  if request.POST :
    raise Http404
  else  :
    f = urllib.urlopen(url)#% params)
  if f is not None :
    s=''
    for line in f.readlines() :
      s+=line.replace('\n','')
    s=keeper(s)
    return HttpResponse(s)

    

def keeper(json) : 
  for field in privateFields :
    #"reString=',"('+field+')":(("[0-9A-Za-z\-@\.]+")|(null)|(true)|(false))'
    json=fieldRe.sub('',json)
  return json
  


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
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
