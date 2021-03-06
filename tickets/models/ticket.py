from datetime import timedelta

from django.db import models
from django.utils import timezone

from tickets.choices import TicketsType
from tickets.managers.ticket import TicketQuerySet
from tickets.models.event import Event
from users.models import User


class Ticket(models.Model):
    event = models.ForeignKey(Event, verbose_name="Event", on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, related_name="tickets")
    is_paid = models.BooleanField("Is ticket paid", default=False)
    is_reserved = models.BooleanField("Is ticket reserved", default=False)
    is_disabled = models.BooleanField("Is ticket disabled", default=False)
    reservation_expired_at = models.DateTimeField("Reservation expires at", blank=True, null=True)
    type = models.CharField("Ticket type", max_length=30, choices=TicketsType.CHOICES)
    price = models.PositiveSmallIntegerField("Price", default=0)

    objects = TicketQuerySet.as_manager()

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return "{} ticket for event {}".format(self.type, self.event)

    def reserve(self) -> None:
        # Make reservation and set 15 minutes for payment
        self.is_reserved = True
        self.reservation_expired_at = timezone.now() + timedelta(minutes=15)
        self.save()

    def withdrawal(self) -> None:
        self.is_reserved = False
        self.is_paid = True
        self.reservation_expired_at = None
        self.save()

    def disable(self) -> None:
        self.is_reserved = False
        self.is_paid = False
        self.reservation_expired_at = None
        self.is_disabled = True
        self.save()
