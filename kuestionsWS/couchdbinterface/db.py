#Author: RemiBouchar
'''
This file contain the method to create database and query view
'''
from couchdb import *


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

import urllib
def queryView(viewUrl) :
 url=SERVER_URL + viewUrl
 f = urllib.urlopen(url)

class IntegrityConstraintException :
  pass

class IllegalAttempt :
  pass


    
  

    



  
 
    

