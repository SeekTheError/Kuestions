#Author: RemiBouchar
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import  render_to_response
from couchdbinterface.entities import User
import security.userauth as security
import uuid


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
  #user exist, login and password are corect, and the account is activated  
  else : 
    return openSession(request,user) 
  return render_to_response('index.html', {'message': message},context_instance=RequestContext(request))
    
def signout(request) :
  context=RequestContext(request)
  t = loader.get_template('index.html')
  response = HttpResponse(t.render(context))
  sessionId=None
  if request.COOKIES.__contains__(security.COOKIE_KEY) :
    sessionId=request.COOKIES[security.COOKIE_KEY]
  if sessionId :
    user=User(sessionId=sessionId)
    user=user.findBySessionId()
    user.sessionId='XXX'+str(uuid.uuid1())
    user.update()
  response.delete_cookie(security.COOKIE_KEY)
  return response
  
  
from datetime import datetime
from couchdb.mapping import DateTimeField
from util.encode import encode


def openSession(request,user) :
  print 'trying to open session for ',user.login
  t = loader.get_template('index.html')
  sessionExpire = getTomorowDatetime()
  #print sessionExpire
  field=DateTimeField()
  #field._to_
  #user.sessionExpire=sessionExpire
  user.sessionId= encode(user.login+user.email+str(sessionExpire)+str(uuid.uuid1()))
  print user.sessionId
  user.update()
  context=RequestContext(request)
  context['message'] = 'good combination'
  context['sessionIsOpen']=True
  context['user']=security.getUserInfoWrapper(user)
  response= HttpResponse(t.render(context))
  key='kuestions'
  #Todo add an expiration date!
  response.set_cookie(security.COOKIE_KEY, user.sessionId)
  return response
  
from datetime import datetime,timedelta
def getTomorowDatetime() :
  oneDay=timedelta(hours=24)
  now=datetime.now()
  return now+oneDay
  


  