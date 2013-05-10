from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^intranet/', include('intranet.foo.urls')),

    (r'^$', 'views.index_view'),
    
    # login page
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

    # logout page
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    
    (r'^addressbook/', include('addressbook.urls')),
)

if settings.DEV_SITE:
    urlpatterns += patterns('',
     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                            )
