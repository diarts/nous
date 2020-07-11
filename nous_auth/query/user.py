from functools import partial
from databases import Database
from sqlalchemy import select, and_

from .base import rm_object, get_object_by_param, get_object, make_object
from nous_auth.db.models import token, user

__all__ = (
    'rm_token',
    'get_token',
    'get_user',
    'get_user_by_email',
    'get_user_by_phone',
)

rm_token = partial(rm_object, token, token.c.token)
get_token = partial(get_object_by_param, token, token.c.token)
get_user = partial(get_object_by_param, user, user.c.id)
make_token = partial(make_object, token)


async def get_user_by_email(conn: Database, email: str):
    """Get user from DB by bunch his email and his password."""
    query = select([user]).where(user.c.email == email)
    return await get_object(conn, query)


async def get_user_by_phone(conn: Database, phone: int, country: int):
    """Get user from DB by bunch his phone number and password."""
    query = select([user]).where(and_(
        user.c.phone == phone,
        user.c.country == country,
    ))
    return await get_object(conn, query)
