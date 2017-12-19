""" Module for the ResponseReader class """


class ResponseReader(object):
    """
        Helper class for extracting logging-relevant information from HTTP response object
    """

    def get_status_code(self, response):
        """
        get response's integer status code

        :param response:
        """
        raise NotImplementedError

    def get_response_size(self, response):
        """
        get response's size in bytes

        :param response:
        """
        raise NotImplementedError

    # pylint: disable=no-self-use
    def get_content_type(self, response):
        """
        get response's MIME/media type

        :param response:
        """
        return response.content_type
