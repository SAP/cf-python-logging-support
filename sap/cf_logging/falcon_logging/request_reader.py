""" Falcon request reader """

from sap.cf_logging import defaults
from sap.cf_logging.core.request_reader import RequestReader


class FalconRequestReader(RequestReader):
    """ Read log related properties out of falcon request """

    def __init__(self, username_key):
        self._username_key = username_key

    def get_remote_user(self, request):
        user = request.context.get('user')
        if user and self._username_key:
            return user.get(self._username_key) or defaults.UNKNOWN

        return defaults.UNKNOWN

    def get_protocol(self, request):
        return request.scheme

    def get_content_length(self, request):
        # pylint: disable=duplicate-code
        return request.content_length

    def get_remote_ip(self, request):
        # pylint: disable=duplicate-code
        return request.remote_addr

    def get_remote_port(self, request):
        return defaults.UNKNOWN
