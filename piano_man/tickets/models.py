from django.contrib.auth.models import User
from django.db import models

from django_vcs.models import CodeRepository

class Ticket(models.Model):
    repo = models.ForeignKey(CodeRepository, related_name="tickets")
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField()

    title = models.CharField(max_length=150)
    description = models.TextField()

    def __unicode__(self):
        return "%s filed by %s" % (self.title, self.creator)

class TicketOption(models.Model):
    name = models.CharField(max_length=100)

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
    text = models.TextField()

class TicketChangeItem(models.Model):
    ticket_change = models.ForeignKey(TicketChange, related_name="changes")

    option = models.ForeignKey(TicketOption)
    from_text = models.CharField(max_length=255)
    to_text = models.CharField(max_length=255)
