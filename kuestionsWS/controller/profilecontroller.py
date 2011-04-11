from django.http import HttpResponse, Http404
from django.template import Context,RequestContext, loader

from couchdbinterface.couchdblayer import *
import  couchdbinterface.couchdblayer
import security

def current(request) :
  print 'current'
  context = RequestContext(request)
  context=security.addUserInfoToContext(request,context)
  t = loader.get_template('profile.html')
  if context['sessionIsOpen']== True :
    return HttpResponse(t.render(context))
  else : 
    return HttpResponse(t.render(context))
  


def view(request,login) :
  #TODO distinguish those case: the user see his page, the user see another page
  #And : Distinguish GET/POST method (need to split in different method)
  
  context = RequestContext(request)
  context = security.addUserInfoToContext(request,context)
  currentUser=security.getCurrentUser(context)
  if currentUser and currentUser.login == login:
    print currentUser.login
    context['isAdmin']=True
  else :
    user=User(login=login)
    user=user.findByLogin()
    context["user"]=user
  
  t = loader.get_template('profile.html')
  if user != None :    
    return HttpResponse(t.render(context))
  #TODO code the user not found aspect
  else :
    return HttpResponse(t.render(context))
    
    
    
