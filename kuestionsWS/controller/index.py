from django.http import HttpResponse
from django.template import Context, loader

def view(request) :
  return HttpResponse("Hello, world. You're at the kuestion index.")


