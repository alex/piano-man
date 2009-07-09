from django.db import models

class TicketManager(models.Manager):
    def open(self):
        return self.filter(closed=False)
