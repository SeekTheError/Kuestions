from couchdb import *
from couchdb.mapping import *
from couchdblayer import *




class Dao :
  em=CouchDbInterface()
  
  def getEM(self) :
    return self.cdbi

'''
Begin User Part
'''

class User(Document): 
  login=TextField()
  password=TextField()
  type=TextField()
    
 
    
  def __init__(self,login='',password='') :
    self.login=login
    self.password=password
    self.type=type
    
class UserDao (Dao) :
  FIND_BY_LOGIN='function(u) { if(u.type == \'user\') {if( u.login == \'$login\') {emit (u.login,u);}}}'
  
  # param : a login
  # return: either None if nothing found, of just one Document representing the User
  def findUserByLogin (self,login) :
    query=self.FIND_BY_LOGIN.replace('$login',login)
    #print 'running query: ', query
    view= self.em.getViewResultsForQuery(query)
    #print 'number of results: ',len(view)
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      for u in view : return u
    else :
      print 'WARNING: critical error, more than one user for same login'
  
  # param user: a user instance
  def createUser(self,user) :
    if self.findUserByLogin(user.dict[LOGIN]) == None :
      user_doc=self.em.createDocument(user.dict)
      print 'user created ', user_doc
    else :
      print 'a user already exist for login: ',user.dict[LOGIN]
  
  # param: login, the login of the user you want to delete    
  def deleteUser(self,login) :
    user_doc=self.findUserByLogin(login)
    if user_doc == None :
      print 'user not found, nothing will be deleted, loging: ',login
    else :
      self.em.deleteDocumentById(user_doc['id'])
      
  # param: login, the login of the user you want to update    
  def updateUser(self, user) :
    self.em.updateDocument(user)
      
# param : doc, a couchdb Document instance about a user
# return: a user, or none if the provided document is None


def DocumentToUser (doc) :
  if doc != None :
    user=User(doc.value[LOGIN],doc.value[PASSWORD])
    user.dict[ID]=doc.value[ID]
    return user
  else :
    print 'the provided document is null'
  
'''
End User Part
'''

  
