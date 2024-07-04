# alembic/env.py

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.db.models import Base  # Import your SQLAlchemy Base model
from app.db.config import DATABASE_URL  # Ensure DATABASE_URL points to your SQLite database

# Load configuration from alembic.ini
config = context.config

# Use the DATABASE_URL defined in app.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for logging
fileConfig(config.config_file_name)

# Ensure the Base model is used with the engine
target_metadata = Base.metadata

# Run migrations online
def run_migrations_online():
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        context.run_migrations()
    finally:
        connection.close()

# If we're not being run as part of alembic, assume we're running in prod
if context.is_offline_mode():
    run_migrations_online()
else:
    # Alembic works by including this file in it's list of Python modules,
    #   then calling the run_migrations_online function to actually
    #   perform the migrations.
    run_migrations_online()
