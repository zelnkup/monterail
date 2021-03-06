from rest_framework import serializers

from tickets.models import Ticket
from tickets.services.payment import PaymentGateway


class PaymentSerializer(serializers.Serializer):
    currency = serializers.CharField()
    token = serializers.CharField()
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.unpaid())
    amount = serializers.IntegerField()

    def validate(self, attrs):
        ticket = attrs.get("ticket")
        token = attrs.get("token")
        currency = attrs.get("currency")
        amount = attrs.get("amount")
        PaymentGateway().charge(ticket, token, currency, amount)
        return attrs
