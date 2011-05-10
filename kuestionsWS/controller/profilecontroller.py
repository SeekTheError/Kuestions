#Author Remi Bouchar, Uijune Jeong
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from couchdbinterface.entities import User
import  security.userauth as userauth

from settings import *

from forms import *

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
    imageForm = ImageUploadForm()
    context['form'] = imageForm
  else :
    context['isAdmin'] =False
  user = User(login=login)
  user = user.findByLogin()
  if user is None :
    print "not found"
    return userNotFound(request)
  if not user.picture:
    user.picture='default.png'
  if user.picture is None:
    user.picture='default.png'

  context["user"] = user  
  t = loader.get_template('profile.html')
  return HttpResponse(t.render(context))
    
def userNotFound(request):
  t = loader.get_template('error.html')
  context = RequestContext(request)
  context['message'] = "404 - User Not Found"
  return HttpResponse(t.render(context))  


def getCurrentUser(request):
  '''
  this function returns the current user
  '''
  context = RequestContext(request)
  context = userauth.checkSession(request, context)
  currentUser = userauth.getCurrentUser(context)
  return currentUser 

def update(request, type):
  '''
  this function updates the current user information based on input type
  type example: resume, addTopic,
  '''
  if type == 'resume':
    return updateResume(request)
  elif type == 'addTopic':
    return addTopic(request)
  elif type == 'deleteTopic':
    return deleteTopic(request)

def updateResume(request):
  '''
  this function updates user resume with form post data "newResume"
  '''
  currentUser = getCurrentUser(request)
  if currentUser:
    user = User(login=currentUser.login)
    user = user.findByLogin()
    newResume = request.POST['newResume'].decode('UTF-8')
    if newResume:
      user.resume = newResume
      user.update()
  return HttpResponseRedirect('/user/')

def addTopic(request):
  '''
  this function add a new topic with form post data "newTopic"
  '''
  currentUser = getCurrentUser(request)
  if currentUser:
    user = User(login=currentUser.login)
    user = user.findByLogin()
    
    if request.POST['newTopic']:
      newTopic = request.POST['newTopic'].decode('UTF-8')
      print "add Topic:"+newTopic
      topics = user.topics
      if not (newTopic.lower() in (topic.lower() for topic in topics)):
        
        user.topics.append(newTopic)
        user.update()
        print "result: "+str(user.topics)
  return HttpResponseRedirect('/user/')

def deleteTopic(request):
  '''
  this function delete a topic with form post data "deleteTopic"
  '''
  currentUser = getCurrentUser(request)
  if currentUser:
    user = User(login=currentUser.login)
    user = user.findByLogin()
    
    
    if request.POST['deleteTopic']:
      deleteTopic = request.POST['deleteTopic']
      print "del Topic:"+deleteTopic
      topics = user.topics
      user.topics = [topic for topic in topics if deleteTopic.lower() != topic.lower()]
        #if deleteTopic.lower() == topic.lower():
        #  print topics
        #  print topic
      user.update()
      print "result: "+str(user.topics)
  return HttpResponseRedirect('/user/') 


from time import gmtime, strftime

def pictureUpload(request):
  if request.method == 'POST':
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
      currentUser = getCurrentUser(request)
      if currentUser:
        path = "profile/"+currentUser.login+strftime("(%Y-%m-%d_%H.%M.%S)", gmtime())+".jpg"
        destination = open(STATIC_MEDIA_ROOT+"/"+path, 'wb+')
        for chunk in request.FILES['picture'].chunks():
          destination.write(chunk)
        destination.close()
        user = User(login=currentUser.login)
        user = user.findByLogin()
        user.picture=path
        user.update()
  
  return HttpResponseRedirect('/user/') 
