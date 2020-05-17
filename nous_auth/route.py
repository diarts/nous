from aiohttp import web

from .view.user import (
    user_authentication,
    user_authorization,
    token_cancel,
    user_update,
    user_registration,
    user_remove,
)

apis = {
    1: [
        web.get(r'/api/v1/token/{token:\w+}', user_authentication),
        web.delete(r'/api/v1/token/{token:\w+}', token_cancel),

        web.get('/api/v1/user', user_authorization),
        web.post('/api/v1/user', user_registration),
        web.put('/api/v1/user', user_update),
        web.delete(r'/api/v1/user/{user_id:\d+}', user_remove)
    ]
}


def get_routes(version: int = 0):
    """Return routes list for aiohttp application.
    If version is 0 return routes for all apis.
    """
    if not version:
        api = []
        for routes in apis.values():
            api.extend(routes)
    else:
        api = apis[version]

    return api
