from rest_framework import serializers

from tickets.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for list and creation events
    """

    class Meta:
        model = Event
        fields = "__all__"


class EventRetrieveSerializer(serializers.ModelSerializer):
    reserved_tickets = serializers.CharField(source="get_reserved_tickets_info", read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
