from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    ('^admin/', include(admin.site.urls)),
    ('^tickets/', include('tickets.urls')),
    ('^repo/', include('django_vcs.urls')),
    ('^timeline/', include('timeline.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        ('^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
