from django.http import HttpResponse
from django.template import Context, loader

def index(request) :
  return HttpResponse("Hello, world. You're at the kuestion index.")

from couchdbinterface.couchdblayer import *
import  couchdbinterface.couchdblayer
from mailsender.sender import *


def user(request,login) :
  db=getDatabase()
  user=User(login=login)
  user=user.findByLogin()
  t = loader.get_template('viewcontroller/user.html')
  c=Context({'user':user})
  if user != None :
    return HttpResponse(t.render(c))
  else :
    return HttpResponse("User not found: %s" %login)
