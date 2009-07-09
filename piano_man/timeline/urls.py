from django.conf.urls.defaults import *

urlpatterns = patterns('timeline.views',
    url(r'^(?P<slug>[\w-]+)/$', 'timeline', name='timeline'),
)
