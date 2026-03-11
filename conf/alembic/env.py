"""Логика alembic."""

import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection, pool, text
from sqlalchemy.ext.asyncio import async_engine_from_config

from conf.db import Base
from conf.settings import DB_SCHEMA

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, 'DB_USER', os.environ['DB_USER'])
config.set_section_option(section, 'DB_PASSWORD', os.environ['DB_PASSWORD'])
config.set_section_option(section, 'DB_HOST', os.environ['DB_HOST'])
config.set_section_option(section, 'DB_NAME', os.environ['DB_NAME'])

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def include_object(object_, name, type_, reflected, compare_to):  # noqa: ARG001
    """
    Проверка соответствия схемы.

    :param object_:
    :param name:
    :param type_:
    :param reflected:
    :param compare_to:
    :return:
    """

    return not (type_ == "table" and object_.schema != DB_SCHEMA)


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        include_schemas=True,
        version_table_schema=DB_SCHEMA,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migration."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=DB_SCHEMA,
        include_object=include_object,
    )

    connection.execute(
        text('CREATE SCHEMA IF NOT EXISTS "%s"' % DB_SCHEMA)  # noqa: UP031
    )
    connection.execute(text('set search_path to "%s"' % DB_SCHEMA))  # noqa: UP031
    connection.commit()
    connection.dialect.default_schema_name = DB_SCHEMA

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
