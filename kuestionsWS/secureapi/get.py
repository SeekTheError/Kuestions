from django.http import HttpResponse,HttpResponseRedirect
import urllib

COUCHDB_URL='http://127.0.0.1:5984/'

def gate(request) :
  print 'entering'
  #print '\nrequest data\n', request
  url=COUCHDB_URL+request.path.replace('/kuestions/api/user','kuestiondb')
  print 'new url: ',url
  f=None
  # POST not tested
  if request.POST :
    params = urllib.urlencode(request.POST)
    print params
    f = urllib.urlopen(url , params)
  else  :
    f = urllib.urlopen(url)#% params)
  if f is not None :
    s=''
    for line in f.readlines() :
      s+=line.replace('\n','')
    s=keeper(s)
    return HttpResponse(s)
  else :
    return HttpResponse('ERROR')

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
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
