from datetime import datetime

from django.db.models import Count
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from django_vcs.models import CodeRepository

from tickets.filters import filter_for_repo
from tickets.forms import TicketForm, get_ticket_form
from tickets.models import Ticket

def ticket_list(request, slug):
    repo = get_object_or_404(CodeRepository, slug=slug)
    tickets = repo.tickets.all()
    filter = filter_for_repo(repo)(request.GET or None, queryset=tickets)
    return render_to_response([
        'tickets/%s/ticket_list.html' % repo.name,
        'tickets/ticket_list.html',
    ], {'repo': repo, 'filter': filter}, context_instance=RequestContext(request))

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
    TicketDetailForm = get_ticket_form(repo, edit=True)
    if request.method == "POST":
        detail_form = TicketDetailForm(request.POST)
        if detail_form.is_valid():
            detail_form.save(ticket, new=False, user=request.user)
            ticket.save()
            return redirect(ticket)
    else:
        detail_form = TicketDetailForm(initial=dict([
            (selection.option.name, selection.choice_id) for selection in ticket.selections.all()
        ] + [('closed', ticket.closed)]))
    return render_to_response([
        'tickets/%s/ticket_detail.html' % repo.name,
        'tickets/ticket_detail.html',
    ], {'repo': repo, 'ticket': ticket, 'detail_form': detail_form}, context_instance=RequestContext(request))

def nums_for_option(option, qs=None):
    if qs is None:
        qs = option.choices.all()
    qs = qs.annotate(c=Count('ticketoptionselection')).values_list('text', 'c')
    data = sorted(qs, key=lambda o: o[1], reverse=True)
    total = sum([o[1] for o in data])
    return data, total


def ticket_option_charts(request, slug):
    repo = get_object_or_404(CodeRepository, slug=slug)
    options = repo.ticketoption_set.all()
    data = {}
    for option in options:
        data[option.name] = nums_for_option(option)
    return render_to_response([
        'tickets/%s/ticket_option_charts.html' % repo.name,
        'tickets/ticket_option_charts.html'
    ], {'repo': repo, 'data': data}, context_instance=RequestContext(request))

def ticket_option_chart(request, slug, option):
    repo = get_object_or_404(CodeRepository, slug=slug)
    option = get_object_or_404(repo.ticketoption_set, name__iexact=option)
    filter_class = filter_for_repo(repo)
    filter = filter_class(request.GET or None, queryset=repo.tickets.all())
    data, total = nums_for_option(option,
        option.choices.filter(ticketoptionselection__ticket__in=filter.qs)
    )
    context = {
        'repo': repo,
        'option': option,
        'data': data,
        'total': total,
        'options': repo.ticketoption_set.exclude(id=option.id),
        'filter': filter
    }
    return render_to_response([
        'tickets/%s/ticket_option_chart.html' % repo.name,
        'tickets/ticket_option_chart.html',
    ], context, context_instance=RequestContext(request))
