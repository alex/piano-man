from django.conf.urls.defaults import *

ticket_urls = patterns('tickets.views',
    url(r'^$', 'ticket_list', name='ticket_list'),
    url(r'^new/$', 'new_ticket', name='new_ticket'),
    url(r'^(?P<ticket_id>\d+)/$', 'ticket_detail', name='ticket_detail'),
    url(r'^(?P<ticket_id>\d+)/attachment/(?P<attachment_id>\d+)/$', 'ticket_attachment', name='ticket_attachment'),
    url(r'^(?P<ticket_id>\d+)/attachment/new/$', 'ticket_new_attachment', name='ticket_new_attachment'),
    url(r'^reports/$', 'ticket_reports', name='ticket_reports'),
    url(r'^charts/$', 'ticket_option_charts', name='ticket_option_charts'),
    url(r'^charts/(?P<option>[\w-]+)/$', 'ticket_option_chart', name='ticket_option_chart')
)

urlpatterns = patterns('',
    (r'^(?P<slug>[\w-]+)/', include(ticket_urls)),
)
