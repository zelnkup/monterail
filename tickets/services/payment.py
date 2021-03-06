from secrets import compare_digest
from typing import Union

from django.utils import timezone

from tickets.models import Ticket
from tickets.utils.exceptions import (
    CardError,
    PaymentError,
    CurrencyError,
    BalanceError,
    BillingException,
    ReservationError,
)


class PaymentGateway:
    supported_currencies = ["EUR"]

    def charge(self, instance: Ticket, token: str, currency: str, amount: int) -> Union[Ticket, BillingException]:
        print(instance.reservation_expired_at, timezone.now())

        if compare_digest(token, "card_error"):
            raise CardError("Your card has been declined")
        elif compare_digest(token, "payment_error"):
            raise PaymentError("Something went wrong with your transaction")
        elif currency not in self.supported_currencies:
            raise CurrencyError(f"Currency {currency} not supported")
        elif amount < instance.price:
            raise BalanceError("Not enough amount")
        elif instance.reservation_expired_at < timezone.now():
            raise ReservationError("Reservation time expired")
        else:
            return self.withdrawal(instance)

    @staticmethod
    def withdrawal(instance: Ticket) -> Ticket:
        instance.withdrawal()
        return instance
