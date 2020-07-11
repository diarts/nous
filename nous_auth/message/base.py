class RequestMessage:
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
