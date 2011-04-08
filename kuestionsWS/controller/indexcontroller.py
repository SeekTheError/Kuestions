from django.http import HttpResponse
from django.template import RequestContext, loader

def view(request) :
  t = loader.get_template('index.html')
  c=RequestContext(request)
  return HttpResponse(t.render(c))


