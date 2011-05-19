from django.http import HttpResponse
from model.entities import Question, Rating, TimeLineEvent
from security.userauth import checkSession, getCurrentUser
import json

TIMELINE_SIZE = 20

def get(request):
  context = checkSession(request)
  user = getCurrentUser(context)
  if user is None:
    return HttpResponse()
  #first, collectRows
  user = user.findByLogin()
  rows = []
  for questionId in user.followedQuestions:
    t = TimeLineEvent(question=questionId)
    view = t.findByQuestion()
    for row in view.rows :
      rows.append(row)
  
  #then, sort it
  notSorted = True
  max = len(rows)
  while notSorted:
    notSorted = False
    i = 0
    while i < (max - 1) :
      if isSup(rows[i], rows[i + 1]):
        temp = rows[i]
        rows[i] = rows[i + 1]
        rows[i + 1] = temp
        notSorted = True
      i += 1
  #timeline concatenation 
  #create a copy of the list
  temp = []
  for row in rows:
    temp.append(row)
  dir(temp)  
  if len(temp)==0:
    return HttpResponse()
  #the bloc class is used as a data wraper for the timeline info
  class Bloc:
    pass  
  b = Bloc()
  b.questionId = temp[0].value['question']
  results = []
  b.count = 0;
  b.questionTitle = temp[0].value['questionTitle']
  b.date = temp[0].value['eventDate']
  b.users = []
  currentBloc=b
  #concatenate it by continuous block, and count the number of occurencies
  for row in temp:
    if row.value['question'] == currentBloc.questionId:
      currentBloc.count += 1
      if currentBloc.users.__contains__(row.value['user']) == False:
        currentBloc.users.append(row.value['user'])
    else :
      results.append(currentBloc)
      currentBloc = Bloc()
      currentBloc.count = 1
      currentBloc.questionTitle = row.value['questionTitle']
      currentBloc.date = row.value['eventDate']
      currentBloc.questionId = row.value['question']
      currentBloc.users.append(row.value['user'])
  results.append(currentBloc)    
  #generating the final timeline

  timeline = []             
  for item in results:
    timeline.append({'questionTitle':item.questionTitle,
                      'date':item.date, 
                      'questionId':item.questionId,
                      'answerCount':item.count,
                      'users':item.users})
    
  print json.dumps(timeline)
  #limit the size of the time line to 20   
  values = []
  i = 0
  for item in timeline:
    values.append(item)
    if i > TIMELINE_SIZE :
      break
    i += 1;
  return HttpResponse(json.dumps(values))
    
    
def isSup(x, y):
  if x.value.get('_id') > y.value.get('_id'):
    return True
  else :
    return False

def getQuestionTitle(questionId, rows):
  for row in rows:
    if row.value['question'] == questionId:
      return row.value
