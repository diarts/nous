from aiohttp import web
import aiohttp_swagger as swagger

import click
import logging.config

from nous_auth.settings import get_config
from nous_auth.db import get_engine
from nous_auth.route import get_routes

logger = logging.getLogger('auth')


def get_app(config):
    """Configure aiohttp web application."""
    db_configs = config.pop('databases')
    services = config.pop('services')
    auth_db = db_configs['auth-db']
    settings = config.pop('settings')

    app = web.Application()
    app['config'] = config
    app['auth-db'] = get_engine(auth_db)
    app['services'] = services

    app.add_routes(get_routes(settings['api']))
    # добавление автоматической генерации документации для апи
    swagger.setup_swagger(
        app,
        title='API сервиса авторизации.',
        api_version=settings['api'] or 'all versions',
        swagger_url='/api/doc/auth_service',
    )

    return app


@click.group()
def cli():
    pass


@cli.command()
@click.option('--config', default=None, help='path to config file')
def run(config):
    """Starting web application."""
    click.echo('Handle config file.')
    config = get_config(config)
    log_conf = config.pop('logger')
    logging.config.dictConfig(log_conf)

    click.echo('Configure application.')
    app = get_app(config)
    click.echo('Starting application...')
    web.run_app(app)


if __name__ == '__main__':
    cli()
