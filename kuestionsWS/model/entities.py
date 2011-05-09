from couchdb.mapping import *
from couchdbinterface.dblayer import getDb
from couchdbinterface.entities  import User 
from datetime import datetime
import couchdbinterface.dblayer


class Question(Document):
  content = TextField()
  '''
  the login of the asker
  '''
  asker = TextField()
  '''
  a list of topics chose by the user and related to the question
  '''
  topics = ListField(TextField())
  type = TextField()
  TYPE = "question"
  postDate = DateTimeField(default=datetime.now())
  '''
  the number of time a question has been displayed
  '''
  views = IntegerField()
  '''
  poster:the login of the user who post the answer
  content: the content of the answer
  score: the votes on a particular answer
  NOTE: as a user should only vote once on an answer, we should think of a way to enforce that
  '''  
  answers = ListField(DictField(Mapping.build(
         id=TextField(), #id is hash of poster + question
         poster=TextField(),
         content=TextField(),
         time=DateTimeField(default=datetime.now()),
         score=IntegerField(default=0)
     )))

  def create(self) :
    self.type = self.TYPE
    if self.asker == None or self.content == None :
      print "Question: asker or question content cannot be None"
      return None
    u = User(login=self.asker).findByLogin()
    print u.login
    self.asker = u.login
    print u

    if u != None :
      self.store(getDb())
      print self
    else :
      return None

  def update(self):
    '''
    update the question
    '''
    if self.id:
      self.store(getDb())
    else:
      print 'invalid state, attempting to update nonexisting question'
      raise IllegalAttempt

  def findById(self) :
    '''
    return user that matches id
    '''
    view = couchdbinterface.dblayer.view("question/id", self.id)
    if len(view) == 0:
      return None
    elif len(view) == 1:
      for u in view : return Question.load(getDb(), u.id)
    else:
      print 'ERROR: more than one question for this ID'
      raise IntegrityConstraintException
    
class Rating(Document):
  _id = TextField()
  type = TextField()
  TYPE = "rating"
  
  def create(self):
    self.type = self.TYPE
    self.store(getDb())
    
  def findById(self):
    return Rating.load(getDb(), self.id)
