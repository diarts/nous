from time import time as current_time
from logging import getLogger
from json import JSONDecodeError

from aiohttp import web, ClientSession
from marshmallow import ValidationError

from . import generate_token
from nous_auth.schema.user import GetAccount
from nous_auth.schema.user import AccountReg, AccountAuth
from nous_auth.message.logger import DBErrorMessage

from nous_auth.query.user import (
    rm_token,
    get_token,
    get_user,
    get_user_by_email,
    get_user_by_phone,
    make_token,
)

from nous_auth.message import *

logger = getLogger('auth')


async def user_authentication(request: web.Request):
    """
    ---
    description: check token and return user data.
    tags:
    - Get user data by token.
    responses:
        "200":
            description: token is active and return user data.
            schema:
                type: object
                properties:
                    email:
                        type: string
                        description: user email, need for user authorization.
                    username:
                        type: string
                        description: name of user.
                    phone:
                        type: integer
                        description: user phone number without county prefix.
                    create_date:
                        type: integer
                        description: unixtime date of create user account.
                    vip:
                        type: integer
                        description: last end time of vip status.
                    blocked:
                        type: integer
                        description: last end time of user block.
                    role:
                        type: integer
                        description: id of user role.
                    country:
                        type: integer
                        description: user live country phone prefix
        "401":
            description: Token not found, need authorization.
    """
    token = request.match_info['token']
    app = request.app

    try:
        async with app['auth-db'] as conn:
            token_obj = await get_token(conn, token)
    except Exception as err:
        logger.exception(DBErrorMessage(str(err)).message)
        raise web.HTTPInternalServerError()

    # token wasn't exist
    if not token_obj:
        return web.HTTPUnauthorized()

    try:
        async with app['auth-db'] as conn:
            user_obj = await get_user(conn, token_obj.get('user_id'))
    except Exception as err:
        logger.exception(DBErrorMessage(str(err)).message)
        raise web.HTTPInternalServerError()

    user = GetAccount().dump(user_obj)
    return web.json_response(data=user, status=200)


async def token_cancel(request: web.Request):
    """
    ---
    description: remove user token if it exist.
    tags:
    - Remove active token.
    responses:
        "200":
            description: Token removed or wasn't exist.
    """
    token = request.match_info['token']
    app = request.app

    try:
        async with app['auth-db'] as conn:
            await rm_token(conn, token)
    except Exception as err:
        logger.exception(DBErrorMessage(str(err)).message)
        raise web.HTTPInternalServerError()

    # remove token in all services
    for service in app['services'] or ():
        while True:
            async with ClientSession() as session:
                url = service['token_delete'].format(token=token)
                async with session.delete(url) as resp:
                    if resp.status == 200:
                        break

    return web.Response(status=200)


async def user_registration(request: web.Request):
    """Add new user."""
    return web.Response(text='registration')


async def user_authorization(request: web.Request):
    """
    ---
    description: Check user data and generate token
    tags:
        - User authorization
    responses:
        "200":
            description: authorization is successful
            schema:
                type: object
                properties:
                    token:
                        type: string
                        description: new user token
                    email:
                        type: string
                        description: user email, need for user authorization
                    username:
                        type: string
                        description: name of user
                    phone:
                        type: integer
                        description: user phone number without county prefix
                    create_date:
                        type: integer
                        description: unixtime date of create user account
                    vip:
                        type: integer
                        description: last end time of vip status
                    blocked:
                        type: integer
                        description: last end time of user block
                    role:
                        type: integer
                        description: id of user role
                    country:
                        type: integer
                        description: user live country phone prefix
        "400":
            description: incorrect user data.
            schema:
                type: object
                properties:
                    invalid_property:
                        type: string
                        description: invalid sent user pro
                    missed_property:
                        type: array of string
                        description: missed required property
    """
    app = request.app

    try:
        # converting parameters
        try:
            parameters = await request.json()
        except JSONDecodeError as err:
            raise IncorrectJson(err.msg)

        try:
            parameters = AccountAuth(many=False).load(parameters,
                                                      unknown='RAISE')
        except ValidationError as mess:
            raise web.HTTPBadRequest(text=str(mess))

        # find user by password and email or phone number
        password = parameters['password']

        try:
            email = parameters['email']
            try:
                async with app['auth-db'] as conn:
                    user_obj = await get_user_by_email(conn, email)
            except Exception as err:
                logger.exception(DBErrorMessage(str(err)).message)
                raise web.HTTPInternalServerError()

            if not user_obj:
                raise EmailNotFound(email=email)

            if user_obj.get('password') != password:
                raise IncorrectPassword()

        except KeyError:
            country, phone, = parameters['country'], parameters['phone']

            try:
                async with app['auth-db'] as conn:
                    user_obj = await get_user_by_phone(conn, phone, country)
            except Exception as err:
                logger.exception(DBErrorMessage(str(err)).message)
                raise web.HTTPInternalServerError()

            if not user_obj:
                raise PhoneNotFound(country=country, phone=phone)

            if user_obj.get('password') != password:
                raise IncorrectPassword()

        # generate new token
        new_token = {
            'user_id': user_obj.get('id'),
            'token': generate_token(),
            'create_date': current_time(),
        }
        try:
            async with app['auth-db'] as conn:
                await make_token(conn, new_token)
        except Exception as err:
            logger.exception(DBErrorMessage(str(err)).message)
            raise web.HTTPInternalServerError()

        response = GetAccount().dump(user_obj)
        response['token'] = new_token['token']
        response['user_id'] = user_obj.get('id')
        status = 200
    except BadRequestMessage as mess:
        response = mess.json
        status = 400

    return web.json_response(response, status=status)


async def user_update(request: web.Request):
    """Update user data."""
    return web.Response(text='update')


async def user_remove(request: web.Request):
    """Remove user."""
    return web.Response(text='remove')
