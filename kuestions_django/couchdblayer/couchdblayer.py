from couchdb import *

# static function that give a database to the couchdbinterface
def getDatabase (url,dbname) :
  print 'trying to connect to couchdb server with url: ',url
  server=Server(url)
  print 'connection successfuly established'
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

DB_NAME='kuestiondb'
SERVER_URL='http://localhost:5984'

#the database instance
db=getDatabase(SERVER_URL,DB_NAME)

def query (query) :
  try :
    return db.query(query)
  except ServerError :
    print 'ServerError, error in query'


class IntegrityConstraintException :
  pass

class ProtectedException :
  pass

from couchdb.mapping import *
class User(Document) :
  login=TextField()
  password=TextField()
  type=TextField()
  
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
  #to ensure database integrity, it is mandatory to use this method the first time the is a new user
    if user.findByLogin() == None :
      user.type='user'
      user.store(db)
      return user
    else :
      print 'a user already exist for login: ', user.login
      
  def update(self) :
    if self.id :
      self.store(db)
    else :
      print 'invalid state, attemp to update a non existing user'

   
'''
this test highlight the way to create user 

#for a new user :
u=User(login='rem',password='pass')   
print User.create(u)

#to find a user by login(login are unique in the database)
u=User(login='rem')
u=u.findByLogin()

#to update a user(need a existing user):
u=User(login='rem')
u=u.findByLogin()
u.password='strong'
u.update()

'''

def testCouch () :
  #creating a user
  u=User(login='rem',password='pass')   
  print User.create(u) , '\n'
  
  #finding & updating a user
  u=User(login='rem')
  u=u.findByLogin()
  print 'user before update: ', u
  print 'changing password to strong'
  u.password='strong'
  u.update()
  print u.findByLogin()
  print 'changing password to VERYstrong'
  u.password='VERYstrong'
  u.update()
  print u.findByLogin()
  
  #try to update a non existing user
  print '\ntrying to update jose, but he don\'t exist'
  u=User(login='jose',password='de')
  u.update()
 
  
  
    
if __name__ == '__main__' :
  testCouch()
    

  
 
    

