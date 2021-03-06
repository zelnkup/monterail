from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from tickets.models import Ticket
from tickets.tasks import run_cancel_reservation_workload


class TicketSerializer(serializers.ModelSerializer):
    """
    List of tickets, create ticket
    """

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["is_paid", "reservation_expired_at", "price", "is_disabled"]

    def validate(self, attrs):
        event = attrs.get("event")
        ticket_type = attrs.get("type")
        if ticket_type not in event.tickets_type:
            raise serializers.ValidationError({"type": "incorrect type"})
        self.ticket_type_quantity = getattr(event, "{}_tickets_quantity".format(ticket_type))
        if self.ticket_type_quantity == 0:
            raise serializers.ValidationError({"quantity": "Out of tickets"})
        if not event.is_active:
            raise serializers.ValidationError({"event": "Event is inactive"})
        if event.started_at < timezone.now():
            raise serializers.ValidationError({"event": "Event has gone"})
        attrs["price"] = getattr(event, "{}_tickets_price".format(ticket_type))
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.reserve()
        # remove one ticket from event ticket's type quantity
        setattr(
            instance.event,
            "{}_tickets_quantity".format(instance.type),
            self.ticket_type_quantity - 1,
        )
        instance.event.save()
        # disable ticket if will not be paid in 15 minutes
        execute_at = timezone.now() + timedelta(minutes=15)
        run_cancel_reservation_workload.apply_async(args=[instance.id], eta=execute_at)
        return instance


class TicketStatisticSerializer(serializers.Serializer):
    total_quantity = serializers.SerializerMethodField(read_only=True)

    def get_total_quantity(self, instance):
        ticket_type = self.context["request"].query_params.get("ticket_type")
        return Ticket.objects.reserved().filter(type=ticket_type).count()
