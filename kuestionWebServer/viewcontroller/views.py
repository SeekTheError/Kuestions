from django.http import HttpResponse

def index(request) :
  return HttpResponse("Hello, world. You're at the kuestion index.")

from couchdbinterface.couchdblayer import *
import  couchdbinterface.couchdblayer


def user(request,login) :
  db=getDatabase()
  u=User(login=login)
  u=u.findByLogin()
  if u != None :
    return HttpResponse("Found it, user %s" %login)
  else :
    return HttpResponse("User not found: %s" %login)
