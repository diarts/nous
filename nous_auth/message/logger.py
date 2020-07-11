from .base import LoggerMessage


class ErrorLoggerMessage(LoggerMessage):
    """Base class for errors message."""
    _MessageBase = 'UNKNOWN ERROR: {mess}.'


class DBErrorMessage(LoggerMessage):
    """Message for database errors logger messages."""
    _MessageBase = 'DB ERROR: {mess}.'
