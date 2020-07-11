from nous_auth.message.base import RequestMessage

__all__ = [
    'BadRequestMessage',
    'EmailNotFound',
    'PhoneNotFound',
    'IncorrectPassword',
    'MissedParameters',
    'WrongParameter',
]


class BadRequestMessage(RequestMessage):
    """Default bad request message."""
    _code = 20
    _text = 'Simple bad request.'


class EmailNotFound(BadRequestMessage):
    """Bad request message, use when sent user mail not found in DB."""
    _code = 21
    _text = 'User with email: "{email}" not found.'

    def __init__(self, email: str):
        self._text = self.text.format(email=email)


class PhoneNotFound(BadRequestMessage):
    """Bad request message, use when sent user phone not found in DB."""
    _code = 21
    _text = 'User with phone +{country} {phone} not found.'

    def __init__(self, country: int, phone: int):
        self._text = self.text.format(country=country, phone=phone)


class IncorrectPassword(BadRequestMessage):
    """Bad request message, use when sent wrong user password."""
    _code = 22
    _text = 'You sent wrong password.'


class MissedParameters(BadRequestMessage):
    """Bad request message, use when missed one or some parameters in
    request.
    """
    _code = 23
    _text = 'Missed one or many parameters.'

    def __init__(self, *args):
        self._params = args

    @property
    def parameters(self):
        """Parameters getter."""
        return self._params

    @property
    def json(self):
        json = super().json
        json['parameters'] = self._params
        return json


class WrongParameter(MissedParameters):
    """Bad request message, use when parameter data is wrong."""
    _code = 24
    _text = 'Wrong parameter: "{parameter}" data.'

    def __init__(self, parameter: str, text: str):
        self._text = f"{self.text.format(parameter=parameter)} {text}"
        super().__init__(parameter)
