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
  
def createQuestion(title):

  #get a random user as the asker
  userlist = getDb().view('user/login')
  randomAsker = random.choice( userlist.rows ).value['login']
  print randomAsker

  #add topics
  topics = title.replace('?','').split(' ')
  #remove prepositions
  f = open('prepositions')
  prepositions = f.read().splitlines()
  f.close()
  for preposition in prepositions:
    print preposition
    filter(lambda a: a != preposition, topics)
  nontopics = [
    'is',
    'the',
    'what',
    'when',
    'why',
    'how',
    'who',
    'a'
  ]
  for word in nontopics:
    filter(lambda a: a != nontopics, topics)
  print topics
  
  #convert title to unicode
  title = smart_unicode(title, encoding='utf-8', strings_only=False, errors='strict')
  print title

  #create question
  q = Question(asker=randomAsker, title=title, topics=topics)
  print q
  try:
    q = q.create()
  except Exception:
    print Exception
  
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

createQuestion('what is the meaning of life?')
