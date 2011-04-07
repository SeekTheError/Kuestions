"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from couchdbinterface.couchdblayer import *

class SimpleTest(TestCase):
  def test_conect_to_db(self):
    print '\n\n--------------------Running the viewcontroller test -------------------------\n'
    server=getServer('http://127.0.0.1:5984')
    print 'connected to server: ',server
    print 'connection test\nnumber of database in the server :', len(server)
   

