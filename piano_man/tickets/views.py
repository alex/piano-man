from datetime import datetime

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from django_vcs.models import CodeRepository

from tickets.forms import TicketForm, get_ticket_form
from tickets.models import Ticket

def ticket_list(request, slug):
    repo = get_object_or_404(CodeRepository, slug=slug)
    tickets = repo.tickets.all()
    return render_to_response([
        'tickets/%s/ticket_list.html' % repo.name,
        'tickets/ticket_list.html',
    ], {'repo': repo, 'tickets': tickets}, context_instance=RequestContext(request))

def new_ticket(request, slug):
    repo = get_object_or_404(CodeRepository, slug=slug)
    TicketDetailForm = get_ticket_form(repo)
    if request.method == "POST":
        form = TicketForm(request.POST)
        detail_form = TicketDetailForm(request.POST)
        if form.is_valid() and detail_form.is_valid():
            ticket = form.save(commit=False)
            ticket.repo = repo
            ticket.creator = request.user
            ticket.created_at = datetime.now()
            ticket.save()
            detail_form.save(ticket)
            return redirect(ticket)
    else:
        form = TicketForm()
        detail_form = TicketDetailForm()
    return render_to_response([
        'tickets/%s/new_ticket.html' % repo.name,
        'tickets/new_ticket.html',
    ], {'repo': repo, 'form': form, 'detail_form': detail_form}, context_instance=RequestContext(request))

def ticket_detail(request, slug, ticket_id):
    repo = get_object_or_404(CodeRepository, slug=slug)
    ticket = get_object_or_404(repo.tickets.all(), pk=ticket_id)
    TicketDetailForm = get_ticket_form(repo)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        detail_form = TicketDetailForm(request.POST)
        if form.is_valid() and detail_form.is_valid():
            ticket = form.save()
            detail_form.save(ticket, new=False, user=request.user)
            return redirect(ticket)
    else:
        form = TicketForm(instance=ticket)
        detail_form = TicketDetailForm(initial=dict([
            (selection.option.name, selection.choice_id) for selection in ticket.selections.all()
        ]))
    return render_to_response([
        'tickets/%s/ticket_detail.html' % repo.name,
        'tickets/ticket_detail.html',
    ], {'repo': repo, 'ticket': ticket, 'form': form, 'detail_form': detail_form}, context_instance=RequestContext(request))
