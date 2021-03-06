from typing import List, Dict

from django.db import models
from tickets.choices import TicketsType
from tickets.managers.event import EventQuerySet
from tickets.utils.fields import ChoiceArrayField


def get_default_ticket():
    return TicketsType.CHOICES_VALUES


class Event(models.Model):
    title = models.CharField("Title", max_length=100)
    tickets_type = ChoiceArrayField(
        models.CharField(max_length=30, choices=TicketsType.CHOICES),
        verbose_name="Tickets type",
        default=get_default_ticket,
    )

    regular_tickets_quantity = models.PositiveIntegerField("Regular tickets quantity", default=0)
    regular_tickets_price = models.PositiveSmallIntegerField("Regular tickets price", default=0)

    premium_tickets_quantity = models.PositiveIntegerField("Premium tickets quantity", default=0)
    premium_tickets_price = models.PositiveSmallIntegerField("Premium tickets price", default=0)

    vip_tickets_quantity = models.PositiveIntegerField("VIP tickets quantity", default=0)
    vip_tickets_price = models.PositiveSmallIntegerField("VIP tickets price", default=0)

    is_active = models.BooleanField("Is event active", default=False)
    started_at = models.DateTimeField("Event time")

    objects = EventQuerySet.as_manager()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return "Event {}, starts at {}".format(self.title, self.started_at)

    @property
    def get_reserved_tickets_info(self) -> List[Dict[str, int]]:
        """
        reservation tickets information
        """
        tickets_list = []
        for ticket_type in self.tickets_type:
            quantity = self.tickets.reserved().filter(type=ticket_type).count()
            tickets_info = {"{}".format(ticket_type): quantity}
            tickets_list.append(tickets_info)
        return tickets_list
