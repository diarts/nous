import yaml
import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG = pathlib.Path(BASE_DIR) / 'configs' / 'develop.yaml'


def get_settings(path=None):
    path = path or DEFAULT_CONFIG
    with open(path) as file:
        config = yaml.safe_load(file)

    # подключение к БД
    try:
        config['auth-db']['host'] = os.environ['AUTH_HOST']
    except KeyError:
        pass
    try:
        config['auth-db']['port'] = os.environ['AUTH_PORT']
    except KeyError:
        pass
    try:
        config['auth-db']['user'] = os.environ['AUTH_LOGIN']
    except KeyError:
        pass
    try:
        config['auth-db']['password'] = os.environ['AUTH_PASSWORD']
    except KeyError:
        pass
    try:
        config['auth-db']['database'] = os.environ['AUTH_DATABASE']
    except KeyError:
        pass

    return config
