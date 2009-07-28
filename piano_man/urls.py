from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from tickets.urls import ticket_urls

admin.autodiscover()


repo_urls = patterns('',
    url(r'^timeline/$', 'timeline.views.timeline', name='timeline'),
    url(r'^tickets/', include(ticket_urls)),
    url(r'^commit/(?P<commit_id>.*)/$', 'django_vcs.views.commit_detail', name='commit_detail'),
    url(r'^browser/(?P<path>.*)$', 'django_vcs.views.code_browser', name='code_browser'),
)


urlpatterns = patterns('',
    url(r'^$', 'django_vcs.views.repo_list', name='repo_list'),
    url(r'^(?P<slug>[\w-]+)/', include(repo_urls)),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
