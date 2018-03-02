""" Sanic response reader """
from sap.cf_logging.core.response_reader import ResponseReader

CONTENT_LENGTH = 'Content-Length'


class SanicResponseReader(ResponseReader):
    """ Implements Sanic specific `ResponseReader` """

    def get_status_code(self, response):
        return response.status

    def get_response_size(self, response):
        if CONTENT_LENGTH in response.headers:
            return response.headers.get(CONTENT_LENGTH)
        return None
