from couchdbinterface.couchdblayer import User

COOKIE_KEY='kuestions_user'


def addUserInfoToContext (request,context) :
  '''
  add some user information to the context if the user is correctly logged in
  '''
  cookieValue=None
  if request.COOKIES.__contains__(COOKIE_KEY) : 
    cookieValue= request.COOKIES[COOKIE_KEY]
  if cookieValue :
    user=User(sessionId=cookieValue)
    user=user.findBySessionId()
    print 'find user '+ str(user.login)
    if user and checkSessionIsValid(user) :
      context['sessionIsOpen']=True
      context['user']=getUserInfoWrapper(user)
    else :
      context['sessionIsOpen']=False
  else : 
    print 'no kuestion cookie found'
    context['sessionIsOpen']=False
  return context
    

#TODO code this to verify the session didn't expire
def checkSessionIsValid(user) :
  return True
  

def getUserInfoWrapper (user) :
  uiw=User()
  uiw.login=user.login
  uiw.resume=user.resume
  return uiw



