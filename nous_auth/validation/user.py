from trafaret import (
    Dict as Trafaret,
    Email,
    String,
    Int,
    DataError,
)

from nous_auth.const.country import COUNTRY_NUMBERS
from nous_auth.message import MissedParameters, WrongParameter

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
        raise DataError(error='Incorrect phone length.')


def authorization_validation(parameters):
    """Check authorization parameters."""
    try:
        parameters['phone']
    except KeyError:
        try:
            parameters['email']
        except KeyError:
            miss = ['phone']
            if 'country' not in parameters:
                miss.append('email')

            raise MissedParameters(*miss)
    else:
        try:
            parameters['country']
        except KeyError:
            raise MissedParameters('country')
    try:
        password = parameters['password']

        if ' ' in password:
            raise WrongParameter(parameter='password',
                                 text='Password can not contain spaces.')
    except KeyError:
        raise MissedParameters('password')
