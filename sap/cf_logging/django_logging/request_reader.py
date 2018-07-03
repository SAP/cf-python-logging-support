""" Django request reader """

from sap.cf_logging import defaults
from sap.cf_logging.core.request_reader import RequestReader


class DjangoRequestReader(RequestReader):
    """ Read log related properties out of Django request """

    def get_remote_user(self, request):
        return request.META.get('REMOTE_USER') or defaults.UNKNOWN

    def get_protocol(self, request):
        return request.scheme

    def get_content_length(self, request):
        return request.META.get('CONTENT_LENGTH') or defaults.UNKNOWN

    def get_remote_ip(self, request):
        return request.META.get('REMOTE_ADDR')

    def get_remote_port(self, request):
        return request.META.get('SERVER_PORT') or defaults.UNKNOWN
