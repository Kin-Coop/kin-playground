from dataclasses import dataclass

from gql.transport.exceptions import TransportQueryError


class OCException(Exception):
    pass


@dataclass
class KnownOCException(OCException):
    message: str


@dataclass
class Handler:

    @staticmethod
    def preamble(func):
        pass

    @staticmethod
    def response_handler(response: dict):
        return response

    @staticmethod
    def error_message_handler(error_message: str):
        raise KnownOCException(error_message)

    def __init__(self, error_message: str = None):
        self.error_message = error_message

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            self.preamble(func)
            try:
                response = func(*args, **kwargs)
                return self.response_handler(response)
            except TransportQueryError as error:
                if self.error_message and self._is_triggered_by(error):
                    return self.error_message_handler(self.error_message)
                raise OCException(error)
        return wrapped_func

    def _is_triggered_by(self, error: TransportQueryError):
        for e in error.errors:
            if self.error_message in e['message']:
                return True
            return False
