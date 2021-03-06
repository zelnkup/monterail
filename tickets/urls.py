from django.urls import path

from tickets.views.event import EventList, EventCreate, EventRetrieve
from tickets.views.payment import PaymentCreate
from tickets.views.ticket import (
    TicketList,
    TicketCreate,
    TicketRetrieve,
    TicketStatistic,
)

app_name = "tickets"

urlpatterns = [
    path("events/create/", EventCreate.as_view(), name="event-create"),
    path("events/list/", EventList.as_view(), name="events-list"),
    path("events/detail/<pk>/", EventRetrieve.as_view(), name="event-detail"),
    path("list/", TicketList.as_view(), name="user-tickets-list"),
    path("create/", TicketCreate.as_view(), name="ticket-create"),
    path("detail/<pk>/", TicketRetrieve.as_view(), name="ticket-detail"),
    path("statistic/", TicketStatistic.as_view(), name="ticket-statistic"),
    path("payment/create/", PaymentCreate.as_view(), name="payment-create"),
]
