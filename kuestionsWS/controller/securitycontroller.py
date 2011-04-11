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
  
  if user and user.password == password:
    return render_to_response('index.html', {'message': 'good combination '},context_instance=RequestContext(request)) 
  else :
    return render_to_response('index.html', {'message': 'wrong combination'},context_instance=RequestContext(request)) 
