import random
import base64
import string
import hashlib


def generate_token():
    a = ''.join(random.choices(string.ascii_uppercase, k=15))
    a = a.encode('ASCII')
    a = base64.b64encode(a)
    return hashlib.md5(a).hexdigest()
