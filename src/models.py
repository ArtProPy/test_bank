from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from conf.db import Base


class OrderStatus(str, Enum):
    """Статусы заказа."""

    UNPAID = "unpaid"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"


class PaymentType(str, Enum):
    """Типы платежей."""

    CASH = "cash"
    ACQUIRING = "acquiring"


class PaymentStatus(str, Enum):
    """Статусы платежей."""

    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    FAILED = "failed"


class Order(Base):
    """Модель заказа."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.UNPAID)
    payments = relationship("Payment", back_populates="order")

    def update_status(self):
        """
        Обновляет статус заказа в зависимости от сумм всех завершённых платежей.
        """
        total_paid = sum(
            p.amount for p in self.payments if p.status == PaymentStatus.COMPLETED
        )
        if total_paid == 0:
            self.status = OrderStatus.UNPAID
        elif total_paid < self.total_amount:
            self.status = OrderStatus.PARTIALLY_PAID
        else:
            self.status = OrderStatus.PAID


class Payment(Base):
    """Модель платежа."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    type = Column(SQLEnum(PaymentType))
    amount = Column(Float, nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="payments")

    def deposit(self, session):
        """
        Проводит платеж и обновляет статус заказа.

        Args:
            session: SQLAlchemy сессия.

        Raises:
            ValueError: если платеж уже обработан или сумма превышает заказ.

        """
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Payment already processed or refunded")
        total_paid = sum(
            p.amount
            for p in self.order.payments
            if p.status == PaymentStatus.COMPLETED
        )
        if total_paid + self.amount > self.order.total_amount:
            raise ValueError("Payment exceeds order total")
        self.status = PaymentStatus.COMPLETED
        self.updated_at = datetime.utcnow()
        self.order.update_status()
        session.commit()

    def refund(self, session):
        """
        Возвращает платеж и обновляет статус заказа.

        Args:
            session: SQLAlchemy сессия.

        Raises:
            ValueError: если платеж не завершён.

        """
        if self.status != PaymentStatus.COMPLETED:
            raise ValueError("Only completed payments can be refunded")
        self.status = PaymentStatus.REFUNDED
        self.updated_at = datetime.utcnow()
        self.order.update_status()
        session.commit()
