#Author Remi Bouchar
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^kuestions/$', 'controller.indexcontroller.view'),
    
    
    (r'^kuestions/security/in/$', 'security.securitycontroller.signin'),
    (r'^kuestions/security/out/$', 'security.securitycontroller.signout'),
    
    (r'^kuestions/user/(?P<login>\w+)/+$', 'controller.profilecontroller.view'),
    (r'^kuestions/user/$', 'controller.profilecontroller.current'),
    
    (r'^kuestions/register/$', 'security.registercontroller.register'),
    (r'^kuestions/register/(?P<code>\w+)$', 'security.registercontroller.activate'),
    
     #block access to the root
    (r'^kuestions/api/$', 'security.api.keeper'),
    (r'^kuestions/api/', 'security.api.gate'),
    
    (r'^kuestions/search/', 'controller.questioncontroller.search'),
    (r'^kuestions/question/post/$', 'controller.questioncontroller.post'),
    
    (r'^$', 'controller.indexcontroller.redirect'),
   
)
