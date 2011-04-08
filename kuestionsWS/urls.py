from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^kuestions/$', 'controller.indexcontroller.view'),
    (r'^kuestions/user/(?P<login>\w+)$', 'controller.profilecontroller.view'),
    (r'^kuestions/register/$', 'controller.registercontroller.register'),
    (r'^kuestions/register/(?P<code>\w+)$', 'controller.registercontroller.activate'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #(r'^admin/', include(admin.site.urls))
)
