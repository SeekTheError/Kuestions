
#-----------------couchdriver------

from couchdb import *


DB_NAME='kuestiondb'
SERVER_URL='http://localhost:5984'

def getDatabase (dbname=DB_NAME) :
  try :
    db = server[dbname]
    return db
  #if the server already exist
  except ValueError :
    print 'server don\'t exist, creating a new one'
    return server.create(dbname)
  except ResourceNotFound :
    print 'server don\'t exist, creating a new one'
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


#TODO add list field
class User(Document) :
  login=TextField()
  password=TextField()
  #re for mail: '\w*@\w*\.\w*'
  mail=TextField()
  #resume is a kind of description in ram text
  resume=TextField()
  #topics=ListField()
  is_activated=BooleanField()
  
  type=TextField()
  TYPE='user'
  FIND_BY_LOGIN='function(u) { if(u.type == \'user\') {if( u.login == \'$login\') {emit (u.id,u);}}}'
  
  def findByLogin(self) :
    view=query(User.FIND_BY_LOGIN.replace('$login',self.login))
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      for u in view : return User.load(db,u.id)
    else :
      print 'WARNING: critical error, more than one user for same login'
      raise IntegrityConstraintException
    
  
  def create(user) :
  #to ensure database integrity, it is mandatory to use this method the first time to creat a new user
    if user.findByLogin() == None :
      user.type=User.TYPE
      user.store(db)
      return user
    else :
      print 'a user already exist for login: ', user.login
      
  def update(self) :
    if self.id :
      self.store(db)
    else :
      print 'invalid state, attemp to update a non existing user'
      raise  IllegalAttempt
  

    
#Test Purpose


  
 
    

