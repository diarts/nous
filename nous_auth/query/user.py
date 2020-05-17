from functools import partial

from .base import rm_object
from nous_auth.db.models import token

rm_token = partial(rm_object, token, token.c.token)
