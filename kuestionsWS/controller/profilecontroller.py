from django.http import HttpResponse
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
  user=User(login=login)
  user=user.findByLogin()
  t = loader.get_template('profile.html')
  c=Context({'user':user})
  if user != None :
    return HttpResponse(t.render(c))
  else :
    return HttpResponse("User not found: %s" %login)
