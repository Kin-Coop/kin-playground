from gql.transport.exceptions import TransportQueryError


def tolerant_of(error_message):
    def is_acceptable(error: TransportQueryError):
        for e in error.errors:
            if error_message in e['message']:
                return True
            return False

    def wrap(func):
        def wrapped_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TransportQueryError as error:
                if is_acceptable(error):
                    return None
                raise error
        return wrapped_func

    return wrap
