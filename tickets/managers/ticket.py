from django.db import models

__all__ = ("TicketQuerySet",)


class TicketQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(is_paid=True, is_disabled=False)

    def reserved(self):
        return self.filter(is_reserved=True, is_disabled=False)

    def unpaid(self):
        return self.filter(is_paid=False, is_disabled=False)
