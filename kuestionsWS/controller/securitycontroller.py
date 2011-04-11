#Author: RemiBouchar
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import  render_to_response
from couchdbinterface.couchdblayer import User

from util.encode import encode

def signin(request) :
  login=request.POST['login']
  password=request.POST['password']
  user=User(login=login)
  user=user.findByLogin()
  password=encode(password)
  
  if login=='' or password=='' :
    message='Please enter a login and a password'
  elif not user :
    message = 'This account does not exist'
  elif not user.isActivated :
    message= 'This account has not been activated yet'
  elif not user.password == password :
    message= 'wrong login/password combination'
  #user exist, login and password are corect, and it's activated  
  else : 
    return openSession(request,user) 
  return render_to_response('index.html', {'message': message},context_instance=RequestContext(request))
    
from datetime import datetime
from couchdb.mapping import DateTimeField
    
def openSession(request,user) :
  print 'trying to open session for ',user.login
  t = loader.get_template('index.html')
  c=RequestContext(request)
  ''' Todo : code the session aspect 
  sessionExpire = getTomorowDatetime
  field=DateTimeField()
  field._to_
  user.sessionExpire=sessionExpire
  user.sessionId= encode(user.login+user.email+str(sessionExpire))
  user.update()
  '''
  c['message'] = 'good combination'
  response= HttpResponse(t.render(c))
  return response
  
from datetime import datetime,timedelta
def getTomorowDatetime() :
  oneDay=timedelta(days=1)
  now=datetime.now()
  return now+oneDay
