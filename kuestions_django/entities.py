from couchdb import *
from simplejson import *
from couchdblayer import *

class Dao :
  em=CouchDbInterface()
  
  def getEM(self) :
    return self.cdbi

'''
Begin User Part
'''

class User(Document): 
  login=''
  password=''
  id=''
  TYPE='user' 
    
  def __init__(self,login,password) :
    self.login=login
    self.password=password
    self.__dict__['login']=login
    self.__dict__['password']=password
    self.__dict__['type']=self.TYPE
 
    
  def hasDict(self) :
    dict={}
    dict['login']=self.login
    dict['password']=self.password
    
    return self.__dict__
    
  def getUserForDoc(self,user_doc) :
    self.login=user_doc['login']
    self.password=user_doc['password']
    
class UserDao (Dao) :
  FIND_BY_LOGIN='function(d) {if(d.type == \'user\') { if(d.login == \'$login\') emit (d._id,d);}}'
  
  def findUserByLogin (self,login) :
    query=self.FIND_BY_LOGIN.replace('$login',login)
    print 'running query: ', query
    view= self.em.getViewResultsForQuery(query)
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      for u in view : return u
  
  def createUser(self,user) :
    if self.findUserByLogin(user.login) == None :
      user_doc=self.em.createDocument(user.hasDict())
      print 'user created ', user_doc
    else :
      print 'a user already exist for login: ',user.login
      
  def deleteUserByLogin(self,login) :
    user_doc=self.findUserByLogin(login)
    print user_doc
    u=User('','')
    u=u.getUserForDoc(user_doc)
    print u.hasDict
    self.em.deleteDocumentById(user_doc['id'])
      
  
    
'''
End User Part
'''

  
