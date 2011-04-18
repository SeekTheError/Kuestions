from couchdbinterface.entities import User

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
    print 'security: find user '+ str(user.login)
    if user and checkSessionIsNotExpired(user) :
      context['sessionIsOpen']=True
      context['user']=getUserInfoWrapper(user)
    else :
      context['sessionIsOpen']=False
  else : 
    print 'security: no kuestion cookie found'
    context['sessionIsOpen']=False
  return context
  
def getCurrentUser(context) :
  if context['sessionIsOpen'] :
    return context['user']
    

#TODO code this to verify the session didn't expire
def checkSessionIsNotExpired(user) :
  return True
  

def getUserInfoWrapper (user) :
  '''
  This function return a Wrapper from a user contain
  '''
  uiw=User()
  uiw.id=user.id
  uiw.login=user.login
  uiw.resume=user.resume
  return uiw



