from xauth.utils import exceptions


def exception_handler(exception, context):
    return exceptions.exception_handler(exception, context)
