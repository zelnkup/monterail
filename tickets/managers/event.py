from django.db import models

__all__ = ("EventQuerySet",)


class EventQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
