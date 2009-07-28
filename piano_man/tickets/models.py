import datetime

from django.contrib.auth.models import User
from django.db import models

from backstage.utils import cached_attribute
from django_vcs.models import CodeRepository

from tickets.managers import TicketManager

class Ticket(models.Model):
    repo = models.ForeignKey(CodeRepository, related_name="tickets")
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    closed = models.BooleanField(default=False)

    title = models.CharField(max_length=150)
    description = models.TextField()

    objects = TicketManager()

    def __unicode__(self):
        return "%s filed by %s" % (self.title, self.creator)

    @models.permalink
    def get_absolute_url(self):
        return ('ticket_detail', (), {'slug': self.repo.slug, 'ticket_id': self.pk})

class TicketOption(models.Model):
    name = models.CharField(max_length=100)
    repo = models.ForeignKey(CodeRepository)

    def __unicode__(self):
        return self.name

class TicketOptionChoice(models.Model):
    option = models.ForeignKey(TicketOption, related_name="choices")
    text = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s for %s" % (self.text, self.option)

class TicketOptionSelection(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="selections")
    option = models.ForeignKey(TicketOption)
    choice = models.ForeignKey(TicketOptionChoice, null=True)

    def __unicode__(self):
        return "%s for %s for %s" % (self.choice, self.option, self.ticket)

    class Meta:
        unique_together = (
            ('ticket', 'option'),
        )

class TicketChange(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="changes")
    user = models.ForeignKey(User)
    at = models.DateTimeField(default=datetime.datetime.now)
    text = models.TextField()

    def get_absolute_url(self):
        # TODO: return this with an anchor to this item
        return self.ticket.get_absolute_url()

    @cached_attribute
    def closes_ticket(self):
        """
        Returns whether this change closes it's ticket.
        """
        try:
            changes = self.changes.get(option="Status")
            if changes.to_text == "Closed":
                return True
        except TicketChangeItem.DoesNotExist:
            return False

class TicketChangeItem(models.Model):
    ticket_change = models.ForeignKey(TicketChange, related_name="changes")

    option = models.CharField(max_length=100)
    from_text = models.TextField()
    to_text = models.TextField()
