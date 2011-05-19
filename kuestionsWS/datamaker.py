from model.entities import Question
from couchdbinterface.entities import User
from couchdbinterface.dblayer import getDb
from util.encode import encode
from django.utils.encoding import smart_unicode

import random

def createUser(userName):
  u = User(login=userName,email='test@test.com',password=encode('123123'))
  u = u.create()
  u.isActivated=True
  
  #allocate ramdom profile image
  number=random.randrange(1, 30)
  u.picture='profile/'+str(number)+'.jpg'
  u.update()

def createQuestionsFromFile(fileName):
  f = open(fileName)
  questions = f.read().splitlines()
  f.close()

  for question in questions:
    createQuestion(question)

def removeAllQuestions():
  removeAllFromView('question/asker')
  removeAllFromView('timeLineEvent/question')

def removeAllFromView(view):
  db = getDb()
  v = db.view(view)
  for row in v:
    db.delete( db[row.id] )
    print 'deleted id: ' + row.id + ' in view: ' + view

def removeAllUsers():
  removeAllFromView('user/login')
  
def createQuestion(title):
  #get a random user as the asker
  userlist = getDb().view('user/login')
  randomAsker = random.choice( userlist.rows ).value['login']

  #add topics
  topics = title.replace('?','').lower().split(' ')
  #remove prepositions
  f = open('prepositions')
  prepositions = f.read().splitlines()
  f.close()

  for preposition in prepositions:
    topics = [e for e in topics if e != preposition]
  nontopics = [
    'some',
    'is',
    'the',
    'what',
    'when',
    'why',
    'how',
    'who',
    'where',
    'a',
    'this',
    'that',
    'are',
    'i',
    'you',
    'can',
    'do'
  ]
  for word in nontopics:
    topics = [e for e in topics if e != word]
  
  #convert title to unicode
  title = smart_unicode(title, encoding='utf-8', strings_only=False, errors='strict')

  #create question
  q = Question(asker=randomAsker, title=title, topics=topics)
  print '********** creating question ***********\n' + 'title: ' + title + '\nasker: ' + randomAsker + '\ntopics: ' + str(topics)
  q.create()
  q.update()

def createInitialUserList():
  username = ''
  profileImgCount = 1
  f = open('/Users/macuser/Kuestions/kuestionsWS/userlist')
  for line in f:
    username = line.replace('\n', '')
    u = User(login=username,email='test@test.com',password=encode('123123'))
    u = u.create()
    u.isActivated=True
    
    #allocate ramdom profile image
    u.picture='profile/'+str(profileImgCount)+'.jpg'
    profileImgCount = profileImgCount + 1
    u.update()
  
  f.close()
