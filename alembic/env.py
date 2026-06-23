import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
sys.path.append(str(Path(__file__).parent.parent))

from app.database.connection import Base
from app.database.connection import DATABASE_URL
from alembic import context
from sqlalchemy import engine_from_config, pool

# IMPORTANTE: Importar los modelos para que Alembic los detecte
from app.models import User, Device, Loan

# Este es el metadata que Alembic necesita
target_metadata = Base.metadata

# Configuración
config = context.config

# Si no se pasó URL por línea de comandos, usar la de DATABASE_URL
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

def run_migrations_offline():
    """Ejecutar migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecutar migraciones en modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()