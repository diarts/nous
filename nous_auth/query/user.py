from functools import partial

from .base import rm_object, get_object
from nous_auth.db.models import token, user

rm_token = partial(rm_object, token, token.c.token)
get_token = partial(get_object, token, token.c.token)
get_user = partial(get_object, user, user.c.id)
