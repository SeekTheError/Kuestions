"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from sender import *

class SimpleTest(TestCase):
    def test_send_mail(self):
      
      sendMail('test','Simple test case:test_send_mail','remi.bouchar@gmail.com')
