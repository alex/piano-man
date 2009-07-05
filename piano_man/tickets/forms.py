from django import forms

from tickets.models import Ticket, TicketOption, TicketOptionChoice, TicketOptionSelection

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']

class TicketDetailForm(forms.Form):
    def save(self, ticket, new=True, commit=True):
        for option in self.fields:
            option = TicketOption.objects.get(name=option)
            choice = TicketOptionChoice.objects.get(pk=self.cleaned_data[option.name], option=option)
            if new:
                TicketOptionSelection.objects.create(ticket=ticket, option=option, choice=choice)
            else:
                updated = TicketOoptionSelect.objects.filter(ticket=ticket, option=option).update(choice=choice)
                if not updated:
                    TicketOptionSelection.objects.create(ticket=ticket, option=option, choice=choice)


def get_ticket_form(repo):
    fields = {}
    for option in TicketOption.objects.filter(repo=repo):
        fields[option.name] = forms.ChoiceField(choices=[(o.id, o.text) for o in option.choices.all()])
    return type('TicketForm', (TicketDetailForm,), fields)
