""" Flask logging context - used by the logging package to keep
request specific data, needed for logging purposes.
For example correlation_id needs to be stored during request processing,
so all log entries contain it.
"""
from flask import g
from sap.cf_logging.core.context import Context


class FlaskContext(Context):
    """ Stores logging context in Flask's request scope """

    def set(self, key, value, request):
        setattr(g, key, value)

    def get(self, key, request):
        return getattr(g, key, None)
