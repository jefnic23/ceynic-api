from enum import Enum


class OrderStatus(Enum):
    CREATED = 1
    SAVED = 2
    APPROVED = 3
    VOIDED = 4
    COMPLETED = 5
    PAYER_ACTION_REQUIRED = 6
    