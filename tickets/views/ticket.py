from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from tickets.choices import TicketsType
from tickets.models import Ticket
from tickets.serializers.ticket import TicketSerializer, TicketStatisticSerializer


class TicketList(generics.ListAPIView):
    """
    Get all user's tickets, filter on paid, reserved and ticket type
    """

    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_paid", "is_reserved", "is_disabled", "type"]

    def get_queryset(self):
        return self.request.user.tickets.all()


class TicketCreate(generics.CreateAPIView):
    """
    Create ticket
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketRetrieve(generics.RetrieveAPIView):
    """
    Get detail info
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketStatistic(generics.GenericAPIView):
    """
    Information about different types of tickets
    """

    serializer_class = TicketStatisticSerializer
    queryset = Ticket.objects.all()

    def get(self, request, *args, **kwargs):
        # get valid types
        valid_types = [x for x, y in TicketsType.CHOICES]
        # check for query param
        if request.query_params.get("ticket_type") not in valid_types:
            return Response(
                "Query param :token_type is required or is incorrect",
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
