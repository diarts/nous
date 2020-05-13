from trafaret import (
    Dict as Trafaret,
    Email,
    String,
    Int,
    DataError,
)

from nous_auth.const.country import COUNTRY_NUMBERS

REGISTER = Trafaret(
    email=Email,
    password=String(allow_blank=False),
    username=String(allow_blank=True, max_length=128),
    phone=Int,
    country=Int,
)


def phone_validation(phone: int = None, country: int = None):
    """Check phone number."""
    if (not phone and country) or (phone and not country):
        raise DataError(error='Missed phone or country number.')

    if country:
        try:
            COUNTRY_NUMBERS[country]
        except KeyError:
            raise DataError(error='Incorrect country number.')

    if len(str(phone)) != 10:
        raise DataError(error='Phone length incorrect.')
