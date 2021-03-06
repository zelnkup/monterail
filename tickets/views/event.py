from rest_framework import generics, permissions

from tickets.models import Event
from tickets.serializers.event import EventSerializer, EventRetrieveSerializer


class EventList(generics.ListAPIView):
    """
    Display all active events
    """

    queryset = Event.objects.active()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventCreate(generics.CreateAPIView):
    """
    Create event
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventRetrieve(generics.RetrieveAPIView):
    """
    Retrieve info about event
    """

    queryset = Event.objects.active()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventRetrieveSerializer
