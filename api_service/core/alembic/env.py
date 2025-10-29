from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from models import models # noqa 
from models.base import Base
from alembic import context
from settings.database_settings import DatabaseSettings
from schemas.sqlalchemy_templates.point_template import PointType # noqa

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

db_config = DatabaseSettings()
config.set_main_option("sqlalchemy.url", db_config.pg_link.render_as_string(hide_password=False) + "?async_fallback=True")

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            compare_type=True,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
