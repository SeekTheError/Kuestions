#Author Remi Bouchar
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from security.userauth import checkSession
from couchdbinterface import dblayer

def view(request) :
  t = loader.get_template('index.html')
  context=RequestContext(request)
  context=checkSession(request,context)
  duplicatedTopics=dblayer.view('topics/topic')
  topics=[]
  for row in duplicatedTopics.view().rows:
    if topics.__contains__(row.key)==False:
      topics.append(row.key)
  context['topics']=topics
  
  return HttpResponse(t.render(context))



