#Author Remi Bouchar
from django.http import HttpResponse
from django.template import RequestContext, loader
from security.userauth import addUserInfoToContext

def view(request) :
  t = loader.get_template('index.html')
  context=RequestContext(request)
  context=addUserInfoToContext(request,context)
  return HttpResponse(t.render(context))


