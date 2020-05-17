from aiohttp import web


async def user_authentication(request):
    """Check token and return user data."""
    return web.Response(text='authentication')


async def token_cancel(request):
    """Remove user token if it exist."""
    return web.Response(text='token cancel')


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
