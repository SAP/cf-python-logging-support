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


class LoggingMiddleware:

    def __init__(self, logger='cf.falcon.logger'):
        self.logger = logger

    def process_request(self, req, resp):
        """Process the request before routing it.

        :param req: - Falcon Request object
        :param resp : - Falcon Response object
        """
        framework = cf_logging.framework
        cid = framework.request_reader.get_correlation_id(req)
        framework.context.set('correlation_id', cid, req)
        framework.context.set('request_started_at', datetime.utcnow(), req)
        req.log = lambda msg, lvl=logging.INFO, extra={}: logging.getLogger(
            self.logger).log(lvl, msg, extra=extra.update({REQUEST_KEY: req}) or extra)

    def process_response(self, req, resp, resource, req_succeeded):
        """Post-processing of the response (after routing).

        :param req: - Falcon Request object
        :param resp : - Falcon Response object
        :param resource : - Falcon Resource object to which the request was
            routed
        :param req_succeeded : - True if no exceptions were raised while
            the framework processed and routed the request
        """
        cf_logging.framework.context.set(
            'response_sent_at', datetime.utcnow(), req)
        extra = {REQUEST_KEY: req, RESPONSE_KEY: resp}
        logging.getLogger(self.logger).info('', extra=extra)


def init(app, level=defaults.DEFAULT_LOGGING_LEVEL):
    """ Initializes logging in JSON format.

    :param app: - Falcon application object
    :param level: - valid log level from standard logging package (optional)
    """
    if not isinstance(app, falcon.API):
        raise TypeError('application should be instance of Falcon API')

    framework = Framework(FALCON_FRAMEWORK_NAME, FalconContext(),
                          FalconRequestReader(), FalconResponseReader())
    cf_logging.init(framework, level)
