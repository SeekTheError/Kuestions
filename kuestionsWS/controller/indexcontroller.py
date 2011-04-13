from django.http import HttpResponse
from django.template import RequestContext, loader
import security.userauth

def view(request) :
  t = loader.get_template('index.html')
  context=RequestContext(request)
  context=security.addUserInfoToContext(request,context)
  return HttpResponse(t.render(context))


