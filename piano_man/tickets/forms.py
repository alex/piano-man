from django import forms
from django.utils.datastructures import SortedDict

from tickets.models import Ticket, TicketOption, TicketOptionChoice, TicketOptionSelection, TicketChange

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']

class TicketDetailForm(forms.Form):
    def save(self, ticket, new=True, user=None, commit=True):
        if not new:
            changes = []
        for option in set(self.fields) - set(['comment']):
            option = TicketOption.objects.get(name=option)
            choice = self.cleaned_data[option.name]
            if choice:
                choice = TicketOptionChoice.objects.get(pk=choice, option=option)
            else:
                choice = None
            if new:
                TicketOptionSelection.objects.create(ticket=ticket, option=option, choice=choice)
            else:
                try:
                    from_text = ticket.selections.get(option=option).choice.text
                except (AttributeError, TicketOptionSelection.DoesNotExist):
                    from_text = ''
                to_text = choice.text
                if from_text != to_text:
                    changes.append((option, from_text, to_text))
                updated = TicketOptionSelection.objects.filter(ticket=ticket, option=option).update(choice=choice)
                if not updated:
                    TicketOptionSelection.objects.create(ticket=ticket, option=option, choice=choice)
        if not new and (changes or self.cleaned_data['comment']):
            change = TicketChange.objects.create(ticket=ticket, user=user, text=self.cleaned_data['comment'])
            for option, from_text, to_text in changes:
                change.changes.create(option=option, from_text=from_text, to_text=to_text)


def get_ticket_form(repo, edit=False):
    fields = SortedDict()
    if edit:
        fields['comment'] = forms.CharField(widget=forms.Textarea)
    for option in TicketOption.objects.filter(repo=repo):
        fields[option.name] = forms.ChoiceField(
            choices=[('', 'None')]+[(o.id, o.text) for o in option.choices.all()],
            required=False
        )
    return type('TicketForm', (TicketDetailForm,), fields)
