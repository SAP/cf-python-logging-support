""" Sanic logging context - used by the logging package to keep
request specific data during request processing for logging purposes.
For example correlation_id needs to be stored so all log entries contain it.
"""
from sap.cf_logging.core.context import Context

CONTEXT_NAME = 'cf_logger_context'


def _init_context(request):
    if CONTEXT_NAME not in request:
        request[CONTEXT_NAME] = {}


class SanicContext(Context):
    """ Stores logging context in Sanic's request object """

    def set(self, key, value, request):
        if request is None:
            return None
        _init_context(request)
        request[CONTEXT_NAME][key] = value

    def get(self, key, request):
        if request is None:
            return None
        _init_context(request)
        if key in request[CONTEXT_NAME]:
            return request[CONTEXT_NAME][key]
        return None
