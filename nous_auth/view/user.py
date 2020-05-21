from aiohttp import web, ClientSession

from nous_auth.query.user import rm_token, get_token, get_user
from nous_auth.schema.user import GetAccount


async def user_authentication(request):
    """
    ---
    description: Check token and return user data.
    tags:
    - Get user data by token.
    responses:
        "200":
            description: Token is active and return user data.
            schema:
                type: object
                properties:
                    email:
                        type:
                            - "string"
                            - "null"
                        description: user email, need for user authorization.
                    username:
                        type:
                            - "string"
                            - "null"
                        description: name of user.
                    phone:
                        type:
                            - "int"
                            - "null"
                        description: user phone number without county prefix.
                    create_date:
                        type: int
                        description: unixtime date of create user account.
                    vip:
                        type: int
                        description: last end time of vip status.
                    blocked:
                        type: int
                        description: last end time of user block.
                    role:
                        type: int
                        description: id of user role.
                    country:
                        type: int
                        description: user live country phone prefix
        "204":
            description: Token not found, need authorization.
    """
    token = request.match_info['token']
    app = request.app

    async with app['auth-db'] as conn:
        token_obj = await get_token(conn, token)

        # token wasn't exist
        if not token_obj:
            return web.HTTPNoContent()

        user_obj = await get_user(conn, token_obj.get('user_id'))
        user = GetAccount().dump(user_obj)

    return web.json_response(data=user, status=200)


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
