#Author: RemiBouchar
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import  render_to_response
import logging

logger=logging.getLogger(__name__)

ACTIVATION_LINK_BASE_URL='http://127.0.0.1:8000/kuestions/register/'


from couchdbinterface.couchdblayer import *
from util.encode import encode
import re

def register(request) :
  '''
  Handle a Post request with the following information:
  login, password, email
  '''
  #parameter retrieval
  login=request.POST['login']
  password=request.POST['password']
  email=request.POST['email']
  
  
  #parameter validation
  loginIsValid= re.match('[\w0-9]*',login) and len(login) > 3 and len(login) < 16
  passwordIsValid=len(password) >= 6 
  emailIsValid=re.match('[\w.]*@\w*\.[\w.]*',email)
  
  #encrypt the password with the sha1 function
  password=encode(password)
  logger.info(login+' '+password+' '+email)
  
  if loginIsValid and passwordIsValid and emailIsValid :
     return processFormInformation(login,password,email,request)     
  else :
  #todo, separate error message on login, pass, 
    message='incorect information on the register form login:'+str(loginIsValid)
    message+=' password:'+ str(passwordIsValid)+' email: '+ str(bool(emailIsValid))
    return render_to_response('index.html', {'message': message},context_instance=RequestContext(request))  

def processFormInformation(login,password,email,request) :
  u = User(login=login,email=email,password=password)
  u=u.create()
  if u != None :
    code=sendActivationMail(login,email)
    u.activationCode=code
    u.update()
    message= 'account succesfully created'
  else :
    message= 'error: login name already taken'
  context={'message': message}
  return render_to_response('index.html', context ,context_instance=RequestContext(request))
     
from mailsender.sender import sendMail    
from hashlib import sha1

def sendActivationMail(login,email) :   
  shaSource= login + email
  code=encode(shaSource)
  subject='Activation mail for Kuestions!'
  message= 'Please follow this link to activate your account' 
  #message+= '\n'+'http://127.0.0.1:8000/kuestions/register/'+code
  message+= '\n'+ACTIVATION_LINK_BASE_URL+code
  sendMail(subject,message,email)
  return code
  
  

def activate(request,code) :
  user=User(activationCode=code)
  user=user.findByActivationCode()
  if user != None:
    if user.isActivated == False :
      user.isActivated= True
      user.update()
      message = 'your account have been succesfully activated'
    else :
      message = 'this account have been already activated'
  else :
    message = 'wrong activation link'
  context={'message': message}
  return render_to_response('index.html', context ,context_instance=RequestContext(request))

     
     
     
     
     
     
     
     
     
  
  
  