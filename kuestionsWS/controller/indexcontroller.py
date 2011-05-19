#Author Remi Bouchar
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from security.userauth import checkSession
from couchdbinterface import dblayer
from couchdbinterface.dblayer import getDb

def view(request) :
  t = loader.get_template('index.html')
  context=RequestContext(request)
  context=checkSession(request,context)

  #topics cloud
  db = getDb()
  duplicatedTopics=db.view('topics/cloud')
  topics=[]
  for row in duplicatedTopics:
    topic = row.key[1]
    if topics.__contains__(topic) == False:
      topics.append(topic)
  topics.reverse() #order by views descending

  #only take top 30 topics
  context['topics']=topics[:30]

  if request.GET.__contains__('search'):
    context['search'] = request.GET['search'];
  
  return HttpResponse(t.render(context))

