from django import forms

from tickets.models import Ticket, TicketOption

class BaseTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']

def get_ticket_form(repo):
    fields = {}
    for option in TicketOption.objects.filter(repo=repo):
        fields[option.name] = forms.ChoiceField(choices=[(o.id, o.text) for o in option.choices.all()])
    return type('TicketForm', (BaseTicketForm,), fields)
