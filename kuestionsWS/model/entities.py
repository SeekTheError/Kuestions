from couchdb.mapping import *
from couchdbinterface.dblayer import getDb ,getDocument
from couchdbinterface.entities  import User 
from datetime import datetime


class Question(Document):
  content=TextField()
  asker=TextField()
  topics=ListField(TextField())
  type=TextField()
  postDate = DateTimeField(default=datetime.now())
  TYPE="question"
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
      print "Question: asker or question cannot be None"
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

