from couchdb.mapping import *
from couchdbinterface.dblayer import getDb
from datetime import datetime
import couchdbinterface.dblayer as dblayer


class Question(Document):
  title = TextField()
  description = TextField()
  asker = TextField() #the login of asker
  topics = ListField(TextField()) #list of topics chosen by user and related to question
  type = TextField(default="question")
  postDate = DateTimeField(default=datetime.now())
  views = IntegerField(default=0) #number of times a question has been displayed
  answers = ListField(DictField(Mapping.build(
         id=TextField(), #hash of answer poster + question
         poster=TextField(), #login of user who posts the answer
         content=TextField(),
         time=DateTimeField(default=datetime.now()),
         score=IntegerField(default=0) 
     )))

  def create(self) :
    #check for required fields
    if self.asker == None or self.title == None:
      raise Exception('error in question creation: asker,title fields required')
      return
    self.store( getDb() )

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
    return question that matches id
    '''
    view = dblayer.view("question/id", self.id)
    if len(view) == 0:
      return None
    elif len(view) == 1:
      for u in view : return Question.load(getDb(), u.id)
    else:
      print 'ERROR: more than one question for this ID'
      raise IntegrityConstraintException
    
class TimeLineEvent(Document):
  _id=TextField()
  type = TextField()
  TYPE = "timeLineEvent"
  user =  TextField()
  action = TextField()
  question = TextField()
  questionTitle = TextField()
  answer = TextField()
  eventDate= TextField()
  
  def create(self):
    import time
    import datetime
    self.id=str(100000000000000000000/time.time()).replace('.','')
    self.eventDate=str(datetime.datetime.now())
    self.type = self.TYPE
    self.store(getDb())
    
  def findByQuestion(self) :
    view=dblayer.view("timeLineEvent/question",self.question)
    return view
  

class Rating(Document):
  _id = TextField()
  type = TextField()
  TYPE = "rating"
  
  def create(self):
    self.type = self.TYPE
    self.store(getDb())
    
  def findById(self):
    return Rating.load(getDb(), self.id)
  
