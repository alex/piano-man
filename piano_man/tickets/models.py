import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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
        if self.is_attachment():
            return TicketAttachment.objects.get(
                ticket=self.ticket, uploaded_by=self.user, uploaded_at=self.at,
                description=self.text
            ).get_absolute_url()
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

    @cached_attribute
    def is_attachment(self):
        """
        Returns whether this change is actually an attachment.
        """
        try:
            self.changes.get(option="Attachment")
            return True
        except TicketChangeItem.DoesNotExist:
            return False

class TicketChangeItem(models.Model):
    ticket_change = models.ForeignKey(TicketChange, related_name="changes")

    option = models.CharField(max_length=100)
    from_text = models.TextField()
    to_text = models.TextField()

    def as_text(self):
        if self.option == 'Attachment':
            return 'Added attachment %s' % self.to_text
        return '%s changed from %s to %s' % (self.option, self.from_text or None, self.to_text or None)


class TicketReport(models.Model):
    repo = models.ForeignKey(CodeRepository, related_name='reports')
    name = models.CharField(max_length=100)
    query_string = models.CharField(max_length=255)

    def get_absolute_url(self):
        return "%s?%s" % (
            reverse('ticket_list', kwargs={'slug': self.repo.slug}),
            self.query_string
        )

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_by = models.ForeignKey(User)
    uploaded_at = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        return ('ticket_attachment', (), {
            'slug': self.ticket.repo.slug,
            'ticket_id': self.ticket.pk,
            'attachment_id': self.pk
        })

    def file_name(self):
        return self.file.name[len('attachments/'):]
