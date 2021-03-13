from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from tickets.choices import TicketsType
from tickets.models import Event, Ticket
from users.models import User


class BaseTestCase(APITestCase):
    """
    Main tickets test case
    """

    event_date = timezone.now() + timedelta(days=10)
    late_event_date = timezone.now() - timedelta(days=5)
    INITIAL_EVENT_DATA = {"title": "Event 1", "started_at": event_date, "is_active": True}
    REGULAR_EVENT_DATA = {
        "title": "Event 2",
        "started_at": event_date,
        "is_active": True,
        "regular_tickets_quantity": 100,
        "regular_tickets_price": 20,
    }
    INACTIVE_EVENT_DATA = {"title": "Event 3", "started_at": event_date}
    LATE_EVENT_DATA = {
        "title": "Event 4",
        "started_at": late_event_date,
        "regular_tickets_quantity": 100,
        "regular_tickets_price": 20,
    }
    REGULAR_TICKET_DATA = {"type": TicketsType.REGULAR, "price": 20}
    PREMIUM_TICKET_DATA = {"type": TicketsType.PREMIUM, "price": 20}

    def _map_events(self):
        events = ["event", "regular_event", "inactive_event", "late_event"]
        events_data = ["INITIAL_EVENT_DATA", "REGULAR_EVENT_DATA", "INACTIVE_EVENT_DATA", "LATE_EVENT_DATA"]
        for index, event in enumerate(events):
            # get event data and set created object to class attrs
            value = getattr(self, events_data[index])
            setattr(self, event, Event.objects.create(**value))

    def setUp(self):
        self.username = "test@gmail.com"
        self.password = "HARDpasw123"
        self.user = User.objects.create_user(username=self.username, email=self.username, password=self.password)
        self._map_events()
        self.login()

    def login(self):
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        User.objects.all().delete()
        Event.objects.all().delete()
        Ticket.objects.all().delete()
