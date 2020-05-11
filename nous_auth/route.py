from aiohttp import web

apis = {
    1: [

    ]
}


def get_routes(version: int = 0):
    """Return routes list for aiohttp application.
    If version is 0 return routes for all apis.
    """
    if not apis:
        api = []
        for routes in apis.values():
            api.extend(routes)
    else:
        api = apis[version]

    return api
