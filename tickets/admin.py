from django.contrib import admin

from tickets.models import Event, Ticket


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "started_at", "is_active"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "is_paid", "is_reserved"]
