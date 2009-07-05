from django.conf.urls.defaults import *

urlpatterns = patterns('tickets.views',
    url(r'^(?P<slug>[\w-]+)/$', 'ticket_list', name='ticket_list'),
    url(r'^(?P<slug>[\w-]+)/new/$', 'new_ticket', name='new_ticket'),
    url(r'^(?P<slug>[\w-]+)/(?P<ticket_id>\d+)/$', 'ticket_detail', name='ticket_detail'),
)
