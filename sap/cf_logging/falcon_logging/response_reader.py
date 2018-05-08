""" Falcon response reader """
from sap.cf_logging.core.response_reader import ResponseReader

CONTENT_LENGTH = 'Content-Length'


class FalconResponseReader(ResponseReader):
    """ Read log related properties out of falcon response """

    def get_status_code(self, response):
        return response.status.split(' ', 1)[0]

    def get_response_size(self, response):
        return response.get_header('Content-Length')
