#Author Remi Bouchar
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'controller.indexcontroller.view'),
    
    
    (r'^security/in/$', 'security.securitycontroller.signin'),
    (r'^security/out/$', 'security.securitycontroller.signout'),
    
    (r'^user/(?P<login>\w+)/+$', 'controller.profilecontroller.view'),
    (r'^user/$', 'controller.profilecontroller.current'),
    
    (r'^register/$', 'security.registercontroller.register'),
    (r'^register/(?P<code>\w+)$', 'security.registercontroller.activate'),
    
     #block access to the root
    (r'^api/$', 'security.api.keeper'),
    (r'^api/', 'security.api.gate'),
    
    (r'^search/', 'controller.questioncontroller.search'),
    (r'^question/post/$', 'controller.questioncontroller.post'),
    (r'^question/(?P<question>\w+)/+$', 'controller.questioncontroller.displayQuestion'),
    
  
   
)
