import asyncpg
import logging
import traceback
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def db_connect(config: dict):
    """Обрабатывает подключение к базе данных."""
    try:
        connect = await asyncpg.connect(**config)

        try:
            yield connect
        except Exception as err:
            logger.warning(f'DB CONNECTION EXCEPTION: {err}.')
            pass
        finally:
            await connect.close()

    except Exception as err:
        logger.error(f'DB CONNECTION ERROR: {traceback.print_exc()}.')
        raise err
