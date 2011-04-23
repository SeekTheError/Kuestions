from couchdb.mapping import *
from couchdbinterface.dblayer import getDb ,getDocument
from couchdbinterface.entities  import User 
from datetime import datetime


class Question(Document):
  content=TextField()
  '''
  the login of the asker
  '''
  asker=TextField()
  '''
  a list of topics chose by the user and related to the question
  '''
  topics=ListField(TextField())
  type=TextField()
  TYPE="question"
  postDate = DateTimeField(default=datetime.now())
  '''
  the number of time a question has been displayed
  '''
  views=IntegerField()
  answers = ListField(DictField(Mapping.build(
         poster = TextField(),
         content = TextField(),
         time = DateTimeField(),
         score =IntegerField()
     )))
  
  import datetime
  def create(self) :
    self.type=self.TYPE
    if self.asker == None or self.content == None :
      print "Question: asker or question content cannot be None"
      return None
    u=User(login=self.asker).findByLogin()
    print u.login
    self.asker=u.login
    print u

    if u != None :
      self.store(getDb())
      print self
    else :
      return None

