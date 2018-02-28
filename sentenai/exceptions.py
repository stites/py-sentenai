__all__ = [
    'FlareSyntaxError',
    'status_codes',
    'NotFound',
    'AuthenticationError',
    'SentenaiException'
]


class SentenaiException(Exception):
    """Base class for Sentenai expections."""
    def __init__(self, *args):
        super().__init__(*args)

class APIError(SentenaiException):
    def __init__(self, resp):
        self.response = resp

class FlareSyntaxError(SentenaiException):
    """A Flare Syntax Error exception."""
    def __init__(self, *args):
        super().__init__(*args)

class AuthenticationError(SentenaiException):
    """An Authentication Error exception."""
    def __init__(self, msg, details, *args):
        super().__init__(msg + ": " + details if details else msg)

class NotFound(SentenaiException):
    """A NotFound Exeption."""
    def __init__(self, *args):
        super().__init__(*args)

def status_codes(resp, *args):
    """Throw the proper exception depending on the status code."""

    code = resp.status_code
    if code == 401:
        raise AuthenticationError("Invalid API key", *args)
    elif code >= 500:
        raise SentenaiException("Something went wrong", code, *args)
    elif code == 400:
        raise FlareSyntaxError(*args)
    elif code == 404:
        raise NotFound(*args)
    elif code >= 400:
        raise APIError(resp, code, *args)

def handle(resp):
    """Handle bad status codes"""

    if resp.status_code == 401:
        raise AuthenticationError("Invalid API Key")
    elif resp.status_code == 400:
        raise FlareSyntaxError
    elif resp.status_code < 200 or resp.status_code >= 400:
        raise SentenaiException("Something went wrong. Code: %i" % resp.status_code)
    return resp
