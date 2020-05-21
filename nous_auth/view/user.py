from aiohttp import web, ClientSession

from nous_auth.query.user import rm_token


async def user_authentication(request):
    """Check token and return user data."""
    return web.Response(text='authentication')


async def token_cancel(request):
    """
    ---
    description: Remove user token if it exist.
    tags:
    - Remove active token.
    responses:
        "200":
            description: Token removed or wasn't exist.
    """
    token = request.match_info['token']
    app = request.app

    async with app['auth-db'] as conn:
        await rm_token(conn, token)

    # remove token in all services
    for service in app['services'] or ():
        while True:
            async with ClientSession() as session:
                url = service['token_delete'].format(token=token)
                async with session.delete(url) as resp:
                    if resp.status == 200:
                        break

    return web.Response(status=200)


async def user_registration(request):
    """Add new user."""
    return web.Response(text='registration')


async def user_authorization(request):
    """Check user data and generate token."""
    return web.Response(text='authorization')


async def user_update(request):
    """Update user data."""
    return web.Response(text='update')


async def user_remove(request):
    """Remove user."""
    return web.Response(text='remove')
