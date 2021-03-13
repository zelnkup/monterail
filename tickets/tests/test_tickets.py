from django.urls import reverse
from rest_framework import status

from tickets.tests.base import BaseTestCase


class TicketAPITestCase(BaseTestCase):
    """
    Test creating tickets with different ticket type and event conditions
    """

    ticket_create_url = reverse("tickets:ticket-create")

    def test_create_ticket_correct_type(self):
        """
        Create ticket with correct type for current event
        """
        self.REGULAR_TICKET_DATA["user"] = self.user.pk
        self.REGULAR_TICKET_DATA["event"] = self.regular_event.pk
        response = self.client.post(self.ticket_create_url, self.REGULAR_TICKET_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ticket_incorrect_type(self):
        """
        Create ticket with incorrect type for current event
        """
        self.PREMIUM_TICKET_DATA["user"] = self.user.pk
        self.PREMIUM_TICKET_DATA["event"] = self.regular_event.pk
        response = self.client.post(self.ticket_create_url, self.PREMIUM_TICKET_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_inactive_event(self):
        """
        Create ticket for inactive event
        """
        self.PREMIUM_TICKET_DATA["user"] = self.user.pk
        self.PREMIUM_TICKET_DATA["event"] = self.inactive_event.pk
        response = self.client.post(self.ticket_create_url, self.PREMIUM_TICKET_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_late_event(self):
        """
        Create ticket for finished event
        """
        self.REGULAR_TICKET_DATA["user"] = self.user.pk
        self.REGULAR_TICKET_DATA["event"] = self.late_event.pk
        response = self.client.post(self.ticket_create_url, self.REGULAR_TICKET_DATA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
