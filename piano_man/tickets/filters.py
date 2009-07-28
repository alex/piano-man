from django.db.models import Q
from django.forms import CheckboxSelectMultiple

from filter import FilterSet, MultipleChoiceFilter, BooleanFilter

from tickets.models import Ticket

class TicketChoiceFilter(MultipleChoiceFilter):
    def filter(self, qs, value):
        q = Q()
        for val in value:
            q |= Q(**{
                'selections__option__name': self.name,
                'selections__choice': val
            })
        return qs.filter(q).distinct()


def filter_for_repo(repo, exclude=None):
    filters = {}
    filters['Meta'] = type('Meta', (object,), {'model': Ticket, 'fields': []})
    filters['closed'] = MultipleChoiceFilter(
        label='Status', choices=[(0, 'open',), (1, 'closed')],
        widget=CheckboxSelectMultiple, initial=[0]
    )
    for option in repo.ticketoption_set.all():
        if exclude is None or (option.name not in exclude):
            filters[option.name] = TicketChoiceFilter(
                choices=[(o.id, o.text) for o in option.choices.all()],
                widget=CheckboxSelectMultiple
            )
    return type('TicketFilterSet', (FilterSet,), filters)
