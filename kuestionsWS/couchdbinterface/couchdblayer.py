#Author: RemiBouchar

from couchdb import *


DB_NAME='kuestiondb'
SERVER_URL='http://localhost:5984'

def getDatabase (dbname=DB_NAME) :
  try :
    db = server[dbname]
    return db
  #if the server already exist
  except ValueError :
    print 'database ' + dbname +  ' don\'t exist, creating a new one'
    return server.create(dbname)
  except ResourceNotFound :
    print 'database ' + dbname +  ' don\'t exist, creating a new one'
    return server.create(dbname)  
    
def getServer(url) :
  return Server(url)

#the defaut database 
server=getServer(SERVER_URL)
db=getDatabase(DB_NAME)


def query (query) :
  try :
    return db.query(query)
  except ServerError :
    print 'ServerError, error in query'


class IntegrityConstraintException :
  pass

class IllegalAttempt :
  pass

#-----------------------Entities-------------------------

#-------------------------User---------------------------
from couchdb.mapping import *


#TODO add topics field
class User(Document) :
  login=TextField()
  password=TextField()
  email=TextField()
  resume=TextField()
  activationCode=TextField()
  #topics=ListField()
  isActivated=BooleanField()
  
  type=TextField()
  TYPE='user'
  FIND_BY_LOGIN='function(u) { if(u.type == \'user\') {if( u.login == \'$login\') {emit (u.id,u);}}}'
  FIND_BY_ACTIVATION_CODE='function(u) { if(u.type == \'user\') {if( u.activationCode == \'$activationCode\') {emit (u.id,u);}}}'
  
  def findByLogin(self) :
    view=query(User.FIND_BY_LOGIN.replace('$login',self.login))
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      for u in view : return User.load(db,u.id)
    else :
      print 'WARNING: critical error, more than one user for same login'
      raise IntegrityConstraintException

  def findByActivationCode(self) :
    view=query(User.FIND_BY_ACTIVATION_CODE.replace('$activationCode',self.activationCode))
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      for u in view : return User.load(db,u.id)
    else :
      print 'WARNING: critical error, more than one user with same activation '
      raise IntegrityConstraintException
    
  
  def create(self) :
  #to ensure database integrity, it is mandatory to use this method the first time to creat a new user
    if self.findByLogin() == None :
      self.isActivated=False
      self.type=self.TYPE
      self.store(db)
      return self
    else :
      print 'a user already exist for login: ', self.login
  def update(self) :
    if self.id :
      self.store(db)
    else :
      print 'invalid state, attemp to update a non existing user'
      raise  IllegalAttempt
      

    
    
  

    



  
 
    

