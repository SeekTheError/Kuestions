from django.core.mail import send_mail
import os
from multiprocessing import Process


fromAdress='kuestions.kaist@gmail.com'

def sendMail(subject,message,toAdress)  :
  send_mail(subject, message, fromAdress, [toAdress], fail_silently=False)


def sendMailAsync(subject,message,toAdress) :
  #os.system('python sender.py', subject,' ',message,' ',toAdress)
  param=[subject,message,toAdress]
  
  p=Process(target=sendMail, args=param)
  p.start()
  p.join()
  print 'living the mail sender'
 

