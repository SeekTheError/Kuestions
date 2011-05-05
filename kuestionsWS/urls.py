#Author Remi Bouchar
from django.conf.urls.defaults import *
from django.conf import settings
urlpatterns = patterns('',
    (r'^$', 'controller.indexcontroller.view'),
    
    
    (r'^security/in/$', 'security.securitycontroller.signin'),
    (r'^security/out/$', 'security.securitycontroller.signout'),
    
    (r'^user/picture/upload$','controller.profilecontroller.pictureUpload'),
    (r'^user/update/(?P<type>\w+)$','controller.profilecontroller.update'),
    (r'^user/$', 'controller.profilecontroller.current'),
    (r'^user/(?P<login>\w+)/+$', 'controller.profilecontroller.view'),
    
    (r'^register/$', 'security.registercontroller.register'),
    (r'^register/(?P<code>\w+)$', 'security.registercontroller.activate'),
    
     #block access to the root
    (r'^api/$', 'security.api.keeper'),
    (r'^api/', 'security.api.gate'),
    
    (r'^search/', 'controller.questioncontroller.search'),
    (r'^question/post/$', 'controller.questioncontroller.post'),
    (r'^question/view/$', 'controller.questioncontroller.viewQuestion'),
    (r'^question/postAnswer/$', 'controller.questioncontroller.postAnswer'), 
    (r'^question/(?P<question>\w+)/+$', 'controller.questioncontroller.displayQuestion'),
    
    
    #For static media files
    (r'^kuestions/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_MEDIA_ROOT}),
   
)
