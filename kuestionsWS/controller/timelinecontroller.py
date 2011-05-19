from django.http import HttpResponse
from model.entities import Question,Rating,TimeLineEvent
from security.userauth import checkSession, getCurrentUser
import json

TIMELINE_SIZE=20

def get(request):
  context = checkSession(request)
  user = getCurrentUser(context)
  if user is None:
    return HttpResponse()
  #first, collectRows
  user=user.findByLogin()
  rows=[]
  for questionId in user.followedQuestions:
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
  #timeline concatenation 
  #create a copy of the list   
  temp=[]
  for row in rows:
    temp.append(row)
  #sort it  by block
  lastQuestionId=temp[0].value['question']
  i=0
  results={}
  results[lastQuestionId]=1;
  for row in temp:
    print row
    if row.value['question'] == questionId:
      results[lastQuestionId]=results.get(lastQuestionId) + 1
    else :
      lastQuestionId= row.value['question']
      results[lastQuestionId]=1;
  print results
  #limit the size of the time line to 20   
  values=[]
  i=0
  for row in rows :
    values.append(row.value)
    if i > TIMELINE_SIZE :
      break
    i+=1;
  return HttpResponse(json.dumps(values))
    
    
def isSup(x,y):
  if x.value.get('_id')>y.value.get('_id'):
    return True
  else :
    return False
