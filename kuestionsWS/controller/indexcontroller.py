from django.http import HttpResponse
from django.template import Context, loader

def view(request) :
  t = loader.get_template('index.html')
  c=Context()
  return HttpResponse(t.render(c))


