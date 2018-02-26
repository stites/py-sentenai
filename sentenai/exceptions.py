import requests.exceptions as rex

__all__ = [
    'FlareSyntaxError',
    'status_codes',
    'NotFound',
    'AuthenticationError',
    'SentenaiException',
    'req_session_handler'
]


class SentenaiException(Exception):
    """Base class for Sentenai expections."""

    pass

class APIError(SentenaiException):
    def __init__(self, resp):
        self.response = resp

class FlareSyntaxError(SentenaiException):
    """A Flare Syntax Error exception."""

    pass


class AuthenticationError(SentenaiException):
    """An Authentication Error exception."""

    pass


class NotFound(SentenaiException):
    """A NotFount Exeption."""

    pass

def status_codes(resp):
    """Throw the proper exception depending on the status code."""

    code = resp.status_code
    if code == 401:
        raise AuthenticationError("Invalid API key")
    elif code >= 500:
        raise SentenaiException("Something went wrong")
    elif code == 400:
        raise FlareSyntaxError()
    elif code == 404:
        raise NotFound()
    elif code >= 400:
        raise APIError(resp)

def handle(resp):
    """Handle bad status codes"""

    if resp.status_code == 401:
        raise AuthenticationError("Invalid API Key")
    elif resp.status_code == 400:
        raise FlareSyntaxError
    elif resp.status_code < 200 or resp.status_code >= 400:
        raise SentenaiException("Something went wrong. Code: %i" % resp.status_code)
    return resp

def req_session_handler(fun):
    """ A function to catch and handle request exceptions.

    See http://docs.python-requests.org/en/master/_modules/requests/exceptions/
    for current exception cases in requests.
    """
    try:
        return fun()

    except rex.ProxyError:  # < ConnectionError < RequestException
        """a Proxy error happened that requests is aware of"""
        raise
    except rex.SSLError:    # < ConnectionError < RequestException
        """an SSL error happened that requests is aware of"""
        raise

    except rex.ConnectionError:  # < RequestException, Timeout
        """Could not connect to server"""
        raise

    except rex.RequestException:  # < IOError
        """Something in requests went wrong. RequestException is the top-level requests exception class."""
        raise

    except Exception:
        """Something requests doesn't handle went wrong"""
        raise


