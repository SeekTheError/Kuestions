#Author: RemiBouchar
'''
This module contain the method to create database and query view

the defaut database is load once the module is loaded
'''
from couchdb import *


'''
TODO: externalize this constant using settings.py
'''
DB_NAME='kuestionsdb'
'''
TODO: externalize this constant using setting.py
'''
SERVER_URL='http://localhost:5984/'

def loadDatabase (dbname) :
  '''
  This method aim to load or create any couchdb database in a LOCAL couchdb installation
  '''
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
    
def getServer(url=SERVER_URL) :
  return Server(url)

'''
the current server instance
'''
server=getServer(SERVER_URL)
print 'server_url: ',SERVER_URL
'''
the current db instance
'''
currentDb=loadDatabase(DB_NAME)

'''
a simple get method, that return the current loaded database
'''
def getDb() : return currentDb


def query (query) :
  '''
  this function perform a new javascript query directly in the database,
  thus it's not optimized at all, but for now it will do the trick.
  
  '''
  try :
    return currentDb.query(query)
  except ServerError :
    print 'ServerError, error in query'

import urllib
def queryView(viewUrl,keyValue=None) :
 '''
 This function will query a couchdb view that already exist, thus it will be fully optimized
 the keyValue parameter
 TODO : finish the coding, and add offset parameter 
 '''
 url=SERVER_URL + viewUrl
 f = urllib.urlopen(url)


    
  

    



  
 
    

