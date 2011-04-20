from couchdb.mapping import *
from couchdbinterface.dblayer import getDb ,getDocument


class Question(Document):
  content=TextField()
  asker=TextField()
  tags=ListField(TextField)
  type=TexField()
  TYPE='question'
  
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

