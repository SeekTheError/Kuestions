from couchdblayer import *
from entities import *
from json import *

def main() :
 # basicObjectCreation()
  entityTest()
  
def entityTest() :
  dao=UserDao()
  u=User('rem','mdp')
  dao.createUser(u)
  
def basicObjectCreation() :
  print 'running test BasicObjectCreation'
  cdbi=CouchDbInterface()   
  print cdbi.database 
  object={'txt':'some text'}
  cdbi.createDocument(object)
  #print cdbi.findDocumentById('object')
  #cdbi.deleteDocumentById('object')
  for r in cdbi.getViewResultsForQuery('function (d) {if (d.txt=="some text") emit (d._id,d)}') :
    print
  
if __name__ == '__main__' :
  main()
