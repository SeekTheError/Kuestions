from couchdb import *
import uuid

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

'''
Convention:
return 0 or the object if succes
return None if failure
'''
class CouchDbInterface :

  DB_NAME='kuestiondb'
  SERVER_URL='http://localhost:5984'
  database=getDatabase(SERVER_URL,DB_NAME)

  # param  : content(map), id(string)
  # return : the newly created document, None otherwise
  def createDocument (self,content) :
    try :
      doc=self.database[uuid.uuid1().hex]=content
      return doc
    except ResourceConflict :
      print 'document already exist, creation fail'
      return None;
  
  # param  : id(string)
  # return : a document, or None if not found
  def findDocumentById (self,id) :
    try :
      return self.database[id]
    except ResourceNotFound : 
      print 'fail to find ressource with id: ',id,',Ressource Not Found'
      return None
   
  # param  : id(string)
  # return : 0 if the deletion is succesful , None otherwise
  def deleteDocumentById (self, id) :
    try :
      doc=self.findDocumentById(id);
      print 'deleting the doc with id: ', id
      self.database.delete(doc)
      return 0
    except  ResourceNotFound :
      print 'fail to delete ressource with id: ',id,',Ressource Not Found'
      return None 
      
  def deleteDocument (self, doc) :
    try :
      self.database.delete(doc)
      return 0
    except  ResourceNotFound :
      print 'fail to delete ressource Ressource Not Found'
      return None  


  # param  : query(string),
  # return : an iterable, or None if the query is not well formated
  def getViewResultsForQuery(self,query) :
    try :
      view= self.database.query(query)
      len(view)
      return view
    except ServerError :
      print 'query error'
      return None
      
  
 
    

