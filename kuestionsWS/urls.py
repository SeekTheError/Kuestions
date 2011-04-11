from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^kuestions/$', 'controller.indexcontroller.view'),
    (r'^kuestions/security/in/$', 'controller.securitycontroller.signin'),
    
    (r'^kuestions/user/(?P<login>\w+)$', 'controller.profilecontroller.view'),
    
    (r'^kuestions/register/$', 'controller.registercontroller.register'),
    (r'^kuestions/register/(?P<code>\w+)$', 'controller.registercontroller.activate')
)
