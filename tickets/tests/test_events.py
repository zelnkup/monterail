import json
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from tickets.tests.base import BaseTestCase


class EventAPITestCase(BaseTestCase):
    """
    Test creating and showing correct events
    """

    event_create_url = reverse("tickets:event-create")
    event_list_url = reverse("tickets:events-list")
    event_detail = "tickets:event-detail"
    event_date = timezone.now() + timedelta(days=10)
    SECOND_EVENT_DATA = {"title": "Event 2", "started_at": event_date, "is_active": True}

    def test_unauthorized_create_event(self):
        """
        Create event from anonymous user
        """
        self.client.logout()
        response = self.client.post(self.event_create_url, self.SECOND_EVENT_DATA)
        self.login()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_create_event(self):
        """
        Create event from authorized user
        """
        response = self.client.post(self.event_create_url, self.SECOND_EVENT_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_active_events(self):
        """
        Test get all active events
        """
        self.test_unauthorized_create_event()
        self.test_authorized_create_event()
        response = self.client.get(self.event_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_detail_event(self):
        """
        Test for retrieve event data
        """
        event_detail_url = reverse(self.event_detail, kwargs={"pk": self.event.pk})
        response = self.client.get(event_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get("title"), "Event 1")
        self.assertEqual(json.loads(response.content).get("tickets_type"), ["regular", "premium", "vip"])
