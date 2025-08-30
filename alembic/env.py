from logging.config import fileConfig
from alembic import context
import  asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from app.config import setting
from db.models import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# فقط نام درایور؛ بدون URL کامل
DB_DRIVER = "postgresql+asyncpg"

# پارامترهای اتصال به جای URL
CONNECT_ARGS = {
    "user":     setting.username,
    "password": setting.password,
    "database": setting.database,
    "host":     setting.host,
    "port":     setting.port,
}

def run_migrations_offline():
    # بدون URL؛ فقط نام دیالکت
    context.configure(
        dialect_name="postgresql",
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def _sync_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    engine = create_async_engine(
        f"{DB_DRIVER}://",              # URL خالی؛ فقط درایور
        poolclass=pool.NullPool,
        connect_args=CONNECT_ARGS,      # همه‌چیز از اینجا می‌آید
    )
    async def run():
        async with engine.connect() as conn:
            await conn.run_sync(_sync_migrations)
        await engine.dispose()
    asyncio.run(run())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
