from django.views import generic

from tickets.models import Event, Ticket


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["event"] = Event.objects.active().first()
        ctx["ticket"] = Ticket.objects.first()
        return ctx
