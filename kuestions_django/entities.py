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

class User : 
  login=''
  password=''
  type='user' 
    
  def __init__(self,login,password) :
    self.login=login
    self.password=password
    
  def hasDict(self) :
    dict={}
    dict['login']=self.login
    dict['password']=self.password
    dict['type']=self.type
    return dict
    
class UserDao (Dao) :
  FIND_BY_LOGIN='function(d) { if(d.login == \'$login\') emit (d._id,d);}'
  
  def findUserByLogin (self,login) :
    query=self.FIND_BY_LOGIN.replace('$login',login)
    print 'running query: ', query
    return self.em.getViewResultsForQuery(query)
  
  def createUser(self,user) :
    if len(self.findUserByLogin(user.login)) == 0 :
      user_doc=self.cdbi.createDocument(user.hasDict())
      print 'user created ', user.hasDict()
    else :
      print 'a user already exist for login: ',user.login
      
  def deleteUserByLogin(self,login) :
    user_doc=findUserByLogin(login)
      
  
    
'''
End User Part
'''

  
