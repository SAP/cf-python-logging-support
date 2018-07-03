"""
Django logging context - used by the logging package to keep
request specific data, needed for logging purposes.
For example correlation_id needs to be stored during request processing,
so all log entries contain it.
"""

from sap.cf_logging.core.context import Context


class DjangoContext(Context):
    """ Stores logging context in Django's request objecct """

    def set(self, key, value, request):
        request[key] = value

    def get(self, key, request):
        return request.get(key) if request else None
