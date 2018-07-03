""" Logging support for Falcon https://falconframework.org/ based applications """
import logging
from datetime import datetime

import falcon

from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.falcon_logging.context import FalconContext
from sap.cf_logging.falcon_logging.request_reader import FalconRequestReader
from sap.cf_logging.falcon_logging.response_reader import FalconResponseReader

FALCON_FRAMEWORK_NAME = 'falcon.framework'


class LoggingMiddleware(object):
    """ Falcon logging middleware """

    def __init__(self, logger_name='cf.falcon.logger'):
        self._logger_name = logger_name

    def process_request(self, request, response): # pylint: disable=unused-argument,no-self-use
        """Process the request before routing it.

        :param request: - Falcon Request object
        :param response: - Falcon Response object
        """
        framework = cf_logging.FRAMEWORK
        cid = framework.request_reader.get_correlation_id(request)
        framework.context.set_correlation_id(cid, request)
        framework.context.set('request_started_at', datetime.utcnow(), request)

    def process_response(self, request, response, resource, req_succeeded): # pylint: disable=unused-argument
        """Post-processing of the response (after routing).

        :param request: - Falcon Request object
        :param response: - Falcon Response object
        :param resource: - Falcon Resource object to which the request was routed
        :param req_succeeded: - True if no exceptions were raised while
            the framework processed and routed the request
        """
        cf_logging.FRAMEWORK.context.set(
            'response_sent_at', datetime.utcnow(), request)
        extra = {REQUEST_KEY: request, RESPONSE_KEY: response}
        logging.getLogger(self._logger_name).info('', extra=extra)


def init(app, level=defaults.DEFAULT_LOGGING_LEVEL, username_key='username'):
    """ Initializes logging in JSON format.

    :param app: - Falcon application object
    :param level: - valid log level from standard logging package (optional)
    :param username_key: key used by the framework to get the username
        out of the request user, set in the request context,
        like `request.context.get('user').get(key)`
    """
    if not isinstance(app, falcon.API):
        raise TypeError('application should be instance of Falcon API')

    framework = Framework(FALCON_FRAMEWORK_NAME, FalconContext(),
                          FalconRequestReader(username_key), FalconResponseReader())
    cf_logging.init(framework, level)
