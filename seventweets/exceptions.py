import functools
from abc import ABCMeta


class HttpException(Exception, metaclass=ABCMeta):
    code = 0


class NotFound(HttpException):
    code = 404


class BadRequest(HttpException):
    code = 400


class Unauthorized(HttpException):
    code = 401


def error_handled(f):
    @functools.wraps(f)
    def inner_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except HttpException as e:
            return "Error: " + str(e), e.code
    return inner_f
