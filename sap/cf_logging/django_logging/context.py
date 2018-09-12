"""
Django logging context - used by the logging package to keep
request specific data, needed for logging purposes.
For example correlation_id needs to be stored during request processing,
so all log entries contain it.
"""

from sap.cf_logging.core.context import Context


def _init_context(request):
    if not hasattr(request, 'context'):
        request.context = {}

class DjangoContext(Context):
    """ Stores logging context in Django's request objecct """

    def set(self, key, value, request):
        if request is None:
            return
        _init_context(request)
        request.context[key] = value

    def get(self, key, request):
        if request is None:
            return None
        _init_context(request)
        return request.context.get(key) if request else None
