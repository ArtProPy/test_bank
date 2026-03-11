from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from conf.base_urls import base_routers
from conf.db import async_session, get_db
from src.models import Payment, Order
from src.serializers import PaymentRequest


payment_router = APIRouter(prefix='/payments')


@payment_router.post('/deposit', summary='Создать и провести платеж')
async def create_payment(
    payment_req: PaymentRequest,
    session: AsyncSession = Depends(get_db),
):
    # получаем заказ
    order = await session.get(Order, payment_req.order_id)

    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    if payment_req.amount <= 0:
        raise HTTPException(status_code=400, detail='Amount must be positive')

    # создаем платеж
    payment = Payment(
        order_id=order.id,
        type=payment_req.type,
        amount=payment_req.amount,
    )

    session.add(payment)
    await session.commit()

    try:
        await payment.deposit(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        'payment_id': payment.id,
        'status': payment.status,
        'order_status': order.status,
    }


@payment_router.post('/refund/{payment_id}', summary='Возврат платежа')
async def refund_payment(
    payment_id: int,
    session: AsyncSession = Depends(get_db),
):
    payment = await session.get(Payment, payment_id)

    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')

    try:
        await payment.refund(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        'payment_id': payment.id,
        'status': payment.status,
        'order_status': payment.order.status,
    }