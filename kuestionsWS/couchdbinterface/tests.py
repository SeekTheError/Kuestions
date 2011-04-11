#Author: RemiBouchar
from django.test import TestCase  
from couchdblayer import *
import couchdblayer


TEST_DB_NAME='kuestiondbtest'
def switchToTestDatabase() :
  print '\n------------------Running the couchdbinterface test -------------------------\n'
  print 'switching to test database'
  #easy way to make sure we have a clean database
  db=getDatabase(TEST_DB_NAME)
  couchdblayer.db=db
  print 'DATABASE TEST ENVIRONMENT: ',server,',',db
  
def deleteTestDatabase() :
  print 'deleting the test database: ',TEST_DB_NAME
  server.delete(TEST_DB_NAME)

class SimpleTest(TestCase):

  def test_entity_manipulation(self):
    switchToTestDatabase()
    
    #creating a user
    u=User(login='rem',password='pass')   
    print User.create(u) , '\n'
    self.assertTrue(u.findByLogin()!=None)
  
    #finding & updating a user
    u=User(login='rem')
    u=u.findByLogin()
    print 'user before update: ', u
    print 'changing password to strong'
    u.password='strong'
    u.update()
    u=u.findByLogin()
    print u
    self.assertEqual(u.password,'strong')
    print 'changing password to VERYstrong'
    u.password='VERYstrong'
    u.update()
    u=u.findByLogin()
    print u
    self.assertEqual(u.password,'VERYstrong')
  
    #try to update a non existing user
    print '\ntrying to update jose, but he don\'t exist'
    try :
      u=User(login='jose',password='de')
      u.update()
    except IllegalAttempt :
      print 'catch an Illegal Attempt'
    self.assertEqual(u.findByLogin(),None)
    
    
    deleteTestDatabase()
  '''
  #10s on remi's laptop
  #100ms /creation
  def test_lots_of_entities(self):
    switchToTestDatabase()
    i=0
    login='a'
    while i < 100 :
      u=User(login=login,password='pass')
      User.create(u)
      login+='b'
      i+=1
      
    deleteTestDatabase()
 
  #remi laptop 41ms/update
  def test_lots_of_updates(self):
    switchToTestDatabase()
    u=User(login='rem',password='pass')
    User.create(u)
    u.findByLogin()
    i=0
    while i < 100 :
      u.password=u.password+'x'
      u.update()
      i+=1
      
    deleteTestDatabase()
    
  '''
    


