import logging

import databases

logger = logging.getLogger(__name__)


def get_engine(config: dict) -> databases.Database:
    engine = databases.Database(
        'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['database'],
        ))
    return engine
