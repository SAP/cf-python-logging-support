""" Job logging context - used by the logging package to keep log data """
from sap.cf_logging.core.context import Context


class JobContext(Context):
    """ Stores logging context in dict """

    def __init__(self):
        self._mem_store = {}

    def set(self, key, value, request):
        self._mem_store[key] = value

    def get(self, key, request):
        return self._mem_store[key] if key in self._mem_store else None
