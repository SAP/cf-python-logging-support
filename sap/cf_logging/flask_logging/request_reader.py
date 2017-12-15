""" Flask request reader """
from sap.cf_logging import defaults
from sap.cf_logging.core.request_reader import RequestReader


class FlaskRequestReader(RequestReader):
    """ Reads data from Flask request """

    def get_remote_user(self, request):
        if request.authorization is not None:
            return request.authorization.username

        return defaults.UNKNOWN

    def get_protocol(self, request):
        return request.environ.get('SERVER_PROTOCOL')

    def get_content_length(self, request):
        return request.content_length

    def get_remote_ip(self, request):
        return request.remote_addr

    def get_remote_port(self, request):
        return request.environ.get('REMOTE_PORT')
