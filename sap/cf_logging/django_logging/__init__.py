""" Logging support for Django based applications """
import logging
from datetime import datetime

from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.django_logging.context import DjangoContext
from sap.cf_logging.django_logging.request_reader import DjangoRequestReader
from sap.cf_logging.django_logging.response_reader import DjangoResponseReader

DJANGO_FRAMEWORK_NAME = 'django.framework'


class LoggingMiddleware(object):  # pylint: disable=useless-object-inheritance
    """ Django logging middleware """

    def __init__(self, get_response, logger_name='cf.django.logger'):
        self._logger_name = logger_name
        self._get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self._get_response(request)

        response = self.process_response(request, response)
        return response

    def process_request(self, request):# pylint: disable=no-self-use
        """
        Process the request before routing it.

        :param request: - Django Request object
        """
        framework = cf_logging.FRAMEWORK
        cid = framework.request_reader.get_correlation_id(request)
        framework.context.set_correlation_id(cid, request)
        framework.context.set('request_started_at', datetime.utcnow(), request)

    def process_response(self, request, response):
        """
        Post-processing of the response (after routing).

        :param request: - Django Request object
        :param request: - Django Response object
        """
        cf_logging.FRAMEWORK.context.set(
            'response_sent_at', datetime.utcnow(), request)
        extra = {REQUEST_KEY: request, RESPONSE_KEY: response}
        logging.getLogger(self._logger_name).info('', extra=extra)
        return response


def init(level=defaults.DEFAULT_LOGGING_LEVEL, custom_fields=None):
    """
    Initializes logging in JSON format.

    :param level: - valid log level from standard logging package (optional)
    """
    framework = Framework(DJANGO_FRAMEWORK_NAME, DjangoContext(),
                          DjangoRequestReader(), DjangoResponseReader(),
                          custom_fields=custom_fields)

    cf_logging.init(framework, level)
