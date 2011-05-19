from model.entities import *
from couchdbinterface.entities import User
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
  
def createQuestion():
  asker='ujlikes'
  questionTitle = smart_unicode('title', encoding='utf-8', strings_only=False, errors='strict')
  questionDescription = smart_unicode('description', encoding='utf-8', strings_only=False, errors='strict')
  
  q = Question(asker=asker, title=questionTitle, description=questionDescription)
  q = q.create()
  
  #TODO : add Topic
  
  q.update()
  

for i in range(1,30):
  print i