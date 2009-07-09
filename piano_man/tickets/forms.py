from django import forms
from django.utils.datastructures import SortedDict

from tickets.models import Ticket, TicketOption, TicketOptionChoice, TicketOptionSelection, TicketChange

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']

class TicketDetailForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

    def save(self, ticket, new=True, user=None, commit=True):
        if not new:
            changes = []
        for option in set(self.fields) - set(['comment']):
            option = TicketOption.objects.get(name=option)
            choice = TicketOptionChoice.objects.get(pk=self.cleaned_data[option.name], option=option)
            if new:
                TicketOptionSelection.objects.create(ticket=ticket, option=option, choice=choice)
            else:
                from_text = ticket.selections.get(option=option).choice.text
                to_text = choice.text
                if from_text != to_text:
                    changes.append((option, from_text, to_text))
                updated = TicketOptionSelection.objects.filter(ticket=ticket, option=option).update(choice=choice)
                if not updated:
                    TicketOptionSelection.objects.create(ticket=ticket, option=option, choice=choice)
        if not new and changes:
            change = TicketChange.objects.create(ticket=ticket, user=user, text=self.cleaned_data['comment'])
            for option, from_text, to_text in changes:
                change.changes.create(option=option, from_text=from_text, to_text=to_text)


def get_ticket_form(repo):
    fields = {}
    for option in TicketOption.objects.filter(repo=repo):
        fields[option.name] = forms.ChoiceField(choices=[(o.id, o.text) for o in option.choices.all()])
    klass = type('TicketForm', (TicketDetailForm,), fields)
    keys = klass.base_fields.keys()
    keys.remove('comment')
    keys.insert(0, 'comment')
    klass.base_fields = SortedDict([(k, klass.base_fields[k]) for k in keys])
    return klass
