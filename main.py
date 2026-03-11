"""Запуск приложения."""


import uvicorn

from conf.urls import app as app

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')  # noqa: S104
