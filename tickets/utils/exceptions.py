from rest_framework.exceptions import APIException


class BillingException(APIException):
    message = "billing error"


class CardError(BillingException):
    pass


class PaymentError(BillingException):
    pass


class CurrencyError(BillingException):
    pass


class BalanceError(BillingException):
    pass


class ReservationError(BillingException):
    pass
