from django.contrib import admin

from tickets.models import TicketOption, TicketOptionChoice

class TicketOptionChoiceInline(admin.TabularInline):
    model = TicketOptionChoice

class TicketOptionAdmin(admin.ModelAdmin):
    inlines = [
        TicketOptionChoiceInline
    ]

admin.site.register(TicketOption, TicketOptionAdmin)
