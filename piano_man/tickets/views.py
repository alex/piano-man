from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from django_vcs.models import CodeRepository

from tickets.forms import get_ticket_form
from tickets.models import Ticket

def ticket_list(request, slug):
    repo = get_object_or_404(CodeRepository, slug=slug)
    tickets = repo.tickets.all()
    return render_to_response([
        'tickets/%s/ticket_list.html' % repo.slug,
        'tickets/ticket_list.html',
    ], {'repo': repo, 'tickets': tickets}, context_instance=RequestContext(request))

def new_ticket(request, slug):
    repo = get_object_or_404(CodeRepository, slug=slug)
    TicketForm = get_ticket_form(repo)
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.repo = repo
            ticket.save()
            return redirect(ticket)
    else:
        form = TicketForm()
    return render_to_response([
        'tickets/%s/new_ticket.html' % repo.slug,
        'tickets/new_ticket.html',
    ], {'repo': repo, 'form': form}, context_instance=RequestContext(request))
