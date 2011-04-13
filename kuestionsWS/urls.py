from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^kuestions/$', 'controller.indexcontroller.view'),
    
    (r'^kuestions/security/in/$', 'security.securitycontroller.signin'),
    (r'^kuestions/security/out/$', 'security.securitycontroller.signout'),
    
    (r'^kuestions/user/(?P<login>\w+)/+$', 'controller.profilecontroller.view'),
    (r'^kuestions/user/$', 'controller.profilecontroller.current'),
    
    (r'^kuestions/register/$', 'controller.registercontroller.register'),
    (r'^kuestions/register/(?P<code>\w+)$', 'controller.registercontroller.activate'),
    
    (r'^kuestions/api/get/$', 'security.api.keeper'),
    (r'^kuestions/api/get/', 'security.api.gate'),
)
