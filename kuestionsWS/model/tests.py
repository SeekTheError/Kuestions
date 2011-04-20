"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from entities import Question
from couchdbinterface.tests import *
from couchdbinterface.entities import User

class SimpleTest(TestCase):
  
  def testBasicPersistence(self):
    switchToTestDatabase()  
    u=User(login='asker')
    u.create()
    u=u.findByLogin()
    id=u.id
    print id
    
    q=Question(asker=id,content="To be or not to be?")
    #print "before persistence: ",q
    print q.content
    question=q.create()
    deleteTestDatabase()
