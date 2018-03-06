""" Flask response reader """
from sap.cf_logging.core.response_reader import ResponseReader


class FlaskResponseReader(ResponseReader):
    """ Implements Flask specific `ResponseReader` """

    def get_status_code(self, response):
        return response.status_code

    def get_response_size(self, response):
        return response.calculate_content_length()
