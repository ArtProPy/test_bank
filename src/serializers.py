"""Набор сериалайзеров."""


from pydantic import BaseModel

from src.models import PaymentType


class PaymentRequest(BaseModel):
    """Схема запроса на создание платежа."""

    order_id: int
    type: PaymentType
    amount: float
