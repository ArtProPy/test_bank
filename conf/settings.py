"""Конфигурация приложения."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Загрузка переменных окружения
level = 5
path_env = '.env'
sub_path = '../'

# Загрузка переменных окружения
while not load_dotenv(path_env) and level > 0:
    path_env = f'{sub_path}{path_env}'
    level -= 1

sub_path += '../'

# Данные для подключения БД
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')
DB_NAME = os.getenv('DB_NAME', '')
DB_SCHEMA = os.getenv('DB_SCHEMA', 'public')

# Данные для проведения тестов
if int(os.environ.get('DEBUG', False)):
    DB_NAME += '_test'

# Название проекта
PROJECT = os.getenv('PROJECT', 'test_bank')
DESCRIPTION = os.getenv('DESCRIPTION', '')