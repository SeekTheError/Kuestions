from django.http import HttpResponse
from model.entities import Question,Rating,TimeLineEvent
from security.userauth import checkSession, getCurrentUser
import json

def get(request):
  print 'get'
  context = checkSession(request)
  user = getCurrentUser(context)
  if user is None:
    return HttpResponse()
  #first, collectRows
  user=user.findByLogin()
  rows=[]
  print user.followedQuestions
  for questionId in user.followedQuestions:
    print questionId
    t=TimeLineEvent(question=questionId)
    view=t.findByQuestion()
    for row in view.rows :
      rows.append(row)
  #then, sort it
  notSorted=True
  max=len(rows)
  while notSorted:
    notSorted=False
    i=0
    while i < (max-1) :
      if isSup(rows[i],rows[i+1]):
        temp=rows[i]
        rows[i]=rows[i+1]
        rows[i+1]=temp
        notSorted=True
      i+=1
  print "sorted"
  values=[]
  i=0
  for row in rows :
    values.append(row.value)
    if i > 20 :
      break
    i+=1;
    

  return HttpResponse(json.dumps(values))
    
    
def isSup(x,y):
  if x.value.get('_id')>y.value.get('_id'):
    return True
  else :
    return False
