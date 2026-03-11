"""Формирования приложения."""


from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse

from conf.settings import DESCRIPTION, PROJECT

base_routers = FastAPI(
    title=PROJECT.title().replace('_', ''),
    description=DESCRIPTION,
    version='0.0.1',
    swagger_ui_parameters={'syntaxHighlight': False},
)


def swagger_monkey_patch(*args, **kwargs):
    """Подгрузка скрипта и стилей с другого ресурса для страницы docs."""

    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url='https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/'
        'swagger-ui-bundle.js',
        swagger_css_url='https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.9.0/'
        'swagger-ui.css',
    )


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch


@base_routers.get('/')
async def go_in_docs():
    """Редирект на доки."""
    return RedirectResponse('/docs')
