"""Формирования приложения."""

from conf.base_urls import base_routers
from src.view import payment_router

app = base_routers

# Объединение частей программы в одно целое
# # Подключение пользователей
app.include_router(payment_router)
