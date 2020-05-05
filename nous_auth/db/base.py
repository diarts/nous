import asyncpg
from contextlib import asynccontextmanager


@asynccontextmanager
async def db_connect(config: dict):
    """Обрабатывает подключение к базе данных."""
    connect = await asyncpg.connect(**config)

    try:
        yield connect
    except Exception as err:
        pass
    finally:
        await connect.close()
