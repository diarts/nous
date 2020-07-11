class RequestMessage(Exception):
    """Base request message."""
    _text: str = None
    _code: int = 0

    def __repr__(self):
        return (f'class <{self.__class__}> with code {self.code} '
                f'and message {self.text}.')

    def __str__(self):
        return f'{self.__class__}({self.code}): {self.text}.'

    @property
    def text(self):
        """Text of request message getter."""
        return self._text

    @property
    def code(self):
        """Message code getter."""
        return self._code

    @property
    def json(self):
        """Message code and text in json format getter."""
        return {
            'code': self.code,
            'text': self.text,
        }


class LoggerMessage:
    """Base logger message."""
    _MessageBase = '{mess}.'

    def __init__(self, mess: str):
        self._mess = self._MessageBase.format(mess=mess)

    @property
    def message(self):
        return self._mess

    def __repr__(self):
        return f'<Logger Message> with message: {self.message}'
