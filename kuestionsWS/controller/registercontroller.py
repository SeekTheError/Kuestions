from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import  render_to_response


#TODO : code the activation part !!!!! 

from couchdbinterface.couchdblayer import *
import re

def register(request) :
  #parameter retrieval
  login=request.POST['login']
  password=request.POST['password']
  email=request.POST['email']
  
  #parameter validation
  loginIsValid= re.match('[\w0-9]*',login) and len(login) > 3 and len(login) < 16
  passwordIsValid=len(password) > 8 and len(password) < 16
  emailIsValid=re.match('[\w.]*@\w*\.[\w.]*',email)
  
  if loginIsValid and passwordIsValid and emailIsValid :
     return processFormInformation(login,password,email,request)     
  else :
    message=' incorect information on the register form login:',loginIsValid,' password:',passwordIsValid,' email: ',emailIsValid
    return render_to_response('index.html', {'form_message': message},context_instance=RequestContext(request))

def processFormInformation(login,password,email,request) :
  u = User(login=login,email=email,password=password)
  u=u.create()
  if u != None :
    code=sendActivationMail(login,email)
    u.activationCode=code
    u.update()
    message= 'succesfully create: ',u.login
  else :
    message= 'error: login name already taken'
  context={'form_message': message}
  return render_to_response('index.html', context ,context_instance=RequestContext(request))
     
from mailsender.sender import sendMail    
from hashlib import sha1

def sendActivationMail(login,email) :   
  shaSource= login + email
  code=sha1(shaSource).hexdigest()
  subject='Activation mail for Kuestions!'
  message='here is your activation code, bitch! \n',code, '\n if your to dumb, your login was: ',login
  sendMail(subject,message,email)
  return code
  

     
     
     
     
     
     
     
     
     
  
  
  
