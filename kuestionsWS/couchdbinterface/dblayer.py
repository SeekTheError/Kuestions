#Author: RemiBouchar
'''
This file contain the method to create database and query view
'''
from couchdb import *

DB_NAME='kuestionsdb'
SERVER_URL='http://localhost:5984/'

def loadDatabase (dbname) :
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

#the defaut 
server=getServer(SERVER_URL)
print 'server_url: ',SERVER_URL
currentDb=loadDatabase(DB_NAME)
def getDb() : return currentDb


def query (query) :
  try :
    return currentDb.query(query)
  except ServerError :
    print 'ServerError, error in query'

import urllib
def queryView(viewUrl) :
 url=SERVER_URL + viewUrl
 f = urllib.urlopen(url)


    
  

    



  
 
    

