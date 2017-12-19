""" Sanic request reader """
from sap.cf_logging import defaults
from sap.cf_logging.core.request_reader import RequestReader


class SanicRequestReader(RequestReader):
    """ Reads data from Sanic request """

    def get_remote_user(self, request):
        return defaults.UNKNOWN

    def get_protocol(self, request):
        return defaults.UNKNOWN

    def get_content_length(self, request):
        return defaults.UNKNOWN

    def get_remote_ip(self, request):
        return request.ip[0]

    def get_remote_port(self, request):  # pylint: disable=unused-argument
        return None
