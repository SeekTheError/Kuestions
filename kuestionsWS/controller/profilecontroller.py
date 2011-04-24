#Author Remi Bouchar
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from couchdbinterface.entities import User
import  security.userauth as userauth

def current(request) :
  '''
  this function display the profile page of the current user
  '''
  context = RequestContext(request)
  context = userauth.checkSession(request, context)
  
  if context['sessionIsOpen'] == True :
    login = context['user'].login
    return HttpResponseRedirect('/user/' + login)
  else : 
    return userNotFound(request)
  


def view(request, login) :
  #TODO distinguish those case: the user see his page, the user see another page
  #And : Distinguish GET/POST method (need to split in different method)
  context = RequestContext(request)
  context = userauth.checkSession(request, context)
  currentUser = userauth.getCurrentUser(context)
  context['currentUser']=currentUser
  if currentUser and currentUser.login == login:
    print currentUser.login
    context['isAdmin'] = True
  else :
    user = User(login=login)
    user = user.findByLogin()
    if user is None :
      print "not found"
      return userNotFound(request)
    context["user"] = user
  t = loader.get_template('profile.html')
  return HttpResponse(t.render(context))
    
def userNotFound(request):
  t = loader.get_template('error.html')
  context = RequestContext(request)
  context['message'] = "404 - User Not Found"
  return HttpResponse(t.render(context))  
    
