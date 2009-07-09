from datetime import datetime, timedelta

from django.db.models import Max, Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django_vcs.models import CodeRepository
from tickets.models import Ticket, TicketChange
from pyvcs.commit import Commit

from timeline.utils import merge_sorted_iters

def timeline(request, slug):
    repo = get_object_or_404(CodeRepository, slug=slug)
    since = datetime.now() - timedelta(days=5)
    items = merge_sorted_iters(
        Ticket.objects.filter(created_at__gte=since).order_by('-created_at'),
        TicketChange.objects.filter(at__gte=since).order_by('-at'),
        repo.get_recent_commits(since),
        keys={Ticket: 'created_at', Commit: 'time', TicketChange: 'at'},
        reverse=True,
    )
    return render_to_response([
        'timeline/%s/timeline.html' % repo.name,
        'timeline/timeline.html',
    ], {'repo': repo, 'items': items}, context_instance=RequestContext(request))
