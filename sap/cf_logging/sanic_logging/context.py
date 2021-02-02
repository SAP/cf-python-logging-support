""" Sanic logging context - used by the logging package to keep
request specific data during request processing for logging purposes.
For example correlation_id needs to be stored so all log entries contain it.
"""
from sap.cf_logging.core.context import Context

CONTEXT_NAME = 'cf_logger_context'


class SanicContext(Context):
    """ Stores logging context in Sanic's request object """

    def set(self, key, value, request):
        if request is not None:
            setattr(request.ctx, key, value)

    def get(self, key, request):
        if request is None:
            return None

        return getattr(request.ctx, key, None)
