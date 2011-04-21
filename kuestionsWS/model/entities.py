from couchdb.mapping import *
from couchdbinterface.dblayer import getDb ,getDocument
import datetime


class Question(Document):
  content=TextField()
  asker=TextField()
  topics=ListField(TextField())
  type=TextField()
  postDate = DateTimeField()#datetime.now())
  TYPE="question"
  views=IntegerField()
  answers = ListField(DictField(Mapping.build(
         poster = TextField(),
         content = TextField(),
         time = DateTimeField(),
         postDate = DateTimeField(),
         score =IntegerField()
     )))
  
  
  def create(self) :
    self.type=self.TYPE
    if self.asker == None or self.content == None :
      print "Question: asker or question cannot be None"
      return None
    
    u=getDocument(self.asker)

    if u != None :
      self.store(getDb())
      print self
    else :
      return None

