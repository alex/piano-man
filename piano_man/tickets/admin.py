from django.contrib import admin
from tickets.models import *

class TicketOptionInline(admin.TabularInline):
    model = TicketOption

class TicketAdmin(admin.ModelAdmin):
    pass

class TicketChangeItemInline(admin.TabularInline):
    model = TicketChangeItem

class TicketChangeAdmin(admin.ModelAdmin):
    inlines = [
        TicketChangeItemInline,
    ]

class TicketOptionChoiceInline(admin.TabularInline):
    model = TicketOptionChoice

class TicketOptionAdmin(admin.ModelAdmin):
    inlines = [
        TicketOptionChoiceInline
    ]

admin.site.register(TicketOption, TicketOptionAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketChange, TicketChangeAdmin)
