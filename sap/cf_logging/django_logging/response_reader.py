""" Django response reader """
from sap.cf_logging.core.response_reader import ResponseReader


class DjangoResponseReader(ResponseReader):
    """ Read log related properties out of Django response """

    def get_status_code(self, response):
        return response.status_code

    def get_response_size(self, response):
        return len(response.content)

    def get_content_type(self, response):
        return response.get('Content-Type')
