""" request_reader provides an interface for the RequestReader class """
import uuid

CORRELATION_ID_HEADERS = ['X-Correlation-ID',
                          'X-CorrelationID', 'X-Request-ID', 'X-Vcap-Request-Id']


class RequestReader(object):
    """
        Helper class for extracting logging-relevant information from HTTP request object
    """

    def get_correlation_id(self, request):
        """
        We assume that the request is a valid request object.

        :param request:
        """
        if request is None:
            return None

        for header in CORRELATION_ID_HEADERS:
            value = self.get_http_header(request, header)
            if value is not None:
                return value
        return str(uuid.uuid1())

    # pylint: disable=no-self-use
    def get_http_header(self, request, header_name, default=None):
        """
        get the HTTP header's value given its name

        :param request:
        :param header_name: name of header
        :param default: default value if header is not found
        :return:
        """
        if request is None or not hasattr(request, 'headers'):
            return default

        if header_name in request.headers:
            return request.headers.get(header_name)
        return default

    def get_remote_user(self, request):
        """

        :param request:
        """
        raise NotImplementedError

    def get_protocol(self, request):
        """
        We assume that request is a valid request object.
        Gets the request protocol (e.g. HTTP/1.1).

        :return: The request protocol or None if it cannot be determined
        """
        raise NotImplementedError

    # pylint: disable=no-self-use
    def get_path(self, request):
        """
        We assume that request is a valid request object.
        Gets the request path.

       :return: the request path (e.g. /index.html)
        """
        return request.path

    def get_content_length(self, request):
        """
        We assume that request is a valid request object.
        The content length of the request.

        :return: the content length of the request or None if it cannot be determined
        """
        raise NotImplementedError

    # pylint: disable=no-self-use
    def get_method(self, request):
        """
        We assume that request is a valid request object.
        Gets the request method (e.g. GET, POST, etc.).

        :return: The request method or None if it cannot be determined
        """
        return request.method

    def get_remote_ip(self, request):
        """
        We assume that request is a valid request object.
        Gets the remote IP of the request initiator.

        :return: An ip address or None if it cannot be determined
        """
        raise NotImplementedError

    def get_remote_port(self, request):
        """
        We assume that request is a valid request object.
        Gets the remote port of the request initiator.

        :return: A port or None if it cannot be determined
        """
        raise NotImplementedError
