from celery import shared_task

from tickets.models import Ticket

__all__ = ("run_cancel_reservation_workload",)


@shared_task
def run_cancel_reservation_workload(ticket_id: int) -> None:
    """
    Run this task ETA and if task ain't paid disable it
    """
    instance: Ticket = Ticket.objects.filter(id=ticket_id).first()
    if instance and not instance.is_paid:
        instance.disable()
