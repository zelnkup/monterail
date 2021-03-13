import json
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from tickets.models import Ticket
from tickets.tests.base import BaseTestCase


class PaymentAPITestCase(BaseTestCase):
    """
    Test payments for different types of tickets
    """

    payment_url = reverse("tickets:payment-create")
    ticket_detail = "tickets:ticket-detail"
    REGULAR_TICKET_SUCCESS_PAYMENT_DATA = {"currency": "EUR", "token": "test", "amount": 20}
    REGULAR_TICKET_FAIL_PAYMENT_DATA = {"currency": "EUR", "token": "test", "amount": 10}

    def setUp(self):
        super().setUp()
        self.REGULAR_TICKET_DATA["user"] = self.user
        self.REGULAR_TICKET_DATA["event"] = self.regular_event
        self.regular_ticket = Ticket.objects.create(**self.REGULAR_TICKET_DATA)
        self.less_payment_amount_ticket = Ticket.objects.create(**self.REGULAR_TICKET_DATA)
        self.late_ticket = Ticket.objects.create(**self.REGULAR_TICKET_DATA)
        self.late_ticket.reservation_expired_at = timezone.now() - timedelta(minutes=5)
        self.late_ticket.save()
        self.regular_ticket.reserve()
        self.less_payment_amount_ticket.reserve()

    def test_create_successful_payment(self):
        """
        Test successful payment for ticket
        """
        self.REGULAR_TICKET_SUCCESS_PAYMENT_DATA["ticket"] = self.regular_ticket.pk
        response = self.client.post(self.payment_url, self.REGULAR_TICKET_SUCCESS_PAYMENT_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ticket_late_payment(self):
        """
        Test late payment (>15min) for ticket
        """
        self.REGULAR_TICKET_SUCCESS_PAYMENT_DATA["ticket"] = self.late_ticket.pk
        response = self.client.post(self.payment_url, self.REGULAR_TICKET_SUCCESS_PAYMENT_DATA)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_create_less_amount_payment(self):
        """
        Test fail payment with less amount than price of ticket
        """
        self.REGULAR_TICKET_FAIL_PAYMENT_DATA["ticket"] = self.less_payment_amount_ticket.pk
        response = self.client.post(self.payment_url, self.REGULAR_TICKET_FAIL_PAYMENT_DATA)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_ticket_less_amount_payment(self):
        """
        Test if ticket changed after failed payment
        """
        self.test_create_less_amount_payment()
        ticket_detail_url = reverse(self.ticket_detail, kwargs={"pk": self.less_payment_amount_ticket.pk})
        response = self.client.get(ticket_detail_url)
        response_data = json.loads(response.content)
        self._verify_ticket_data(response_data, False)

    def test_ticket_successful_payment(self):
        """
        Test if ticket changed to is_paid: True after payment
        """
        self.test_create_successful_payment()
        ticket_detail_url = reverse(self.ticket_detail, kwargs={"pk": self.regular_ticket.pk})
        response = self.client.get(ticket_detail_url)
        response_data = json.loads(response.content)
        self._verify_ticket_data(response_data, True)

    def _verify_ticket_data(self, response_data: json, is_success: bool) -> None:
        """
        Validate response Ticket data
        """
        is_reserved = not is_success
        is_disabled = False
        is_paid = is_success
        ticket: Ticket = self.regular_ticket if is_success else self.less_payment_amount_ticket
        self.assertEqual(response_data.get("is_paid"), is_paid)
        self.assertEqual(response_data.get("is_reserved"), is_reserved)
        self.assertEqual(response_data.get("is_disabled"), is_disabled)
        self.assertEqual(response_data.get("id"), ticket.pk)
        self.assertEqual(response_data.get("type"), ticket.type)
