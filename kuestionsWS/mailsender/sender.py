#from django.core.mail import send_mail

fromAdress='kuestions.kaist@gmail.com'
import os

def sendMail(subject,message,toAdress) :
  os.system('python sender.py', subject,' ',message,' ',toAdress)
  #send_mail(subject, message, fromAdress, [toAdress], fail_silently=False)
    
 
 
import smtplib
import sys

def sendMailAsync() :

  print sys.argv[1], ' ',sys.argv[2], ' ',sys.argv[3]

  fromaddr = fromAdress
  toaddrs  = sys.argv[3]

# Add the From: and To: headers at the start!
  msg = sys.argv[2]
  server = smtplib.SMTP('smtp.gmail.com')
  server.set_debuglevel(1)
  server.sendmail(fromaddr, toaddrs, msg)
  server.quit()


if __name__ == '__main__' :
  sendMailAsync()

