#Author Remi Bouchar
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context,RequestContext, loader
from couchdbinterface.entities import User
import  security.userauth as security

def current(request) :
  context = RequestContext(request)
  context=security.addUserInfoToContext(request,context)
  t = loader.get_template('profile.html')
  if context['sessionIsOpen']== True :
    login=context['user'].login
    return HttpResponseRedirect('/kuestions/user/'+login)
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
    context['isAdmin'] = True
  else :
    user=User(login=login)
    user=user.findByLogin()
    context["user"]=user
  t = loader.get_template('profile.html')
  return HttpResponse(t.render(context))
    
    
    
