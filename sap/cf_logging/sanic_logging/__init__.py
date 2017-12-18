""" Flask logging support package
- Configures standard logging package to produce JSON
- Produces info request log entry per request
"""
import logging
from datetime import datetime
from functools import wraps
from sanic import Sanic

from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.sanic_logging.context import SanicContext
from sap.cf_logging.sanic_logging.request_reader import SanicRequestReader
from sap.cf_logging.sanic_logging.response_reader import SanicResponseReader

SANIC_FRAMEWORK_NAME = 'sanic.framework'


def before_request(wrapped):
    """ Use as decorator on Sanic's before_request handler
    Handles correlation_id by setting it in the context for log records
    """

    @wraps(wrapped)
    def _wrapper(request):
        correlation_id = cf_logging.framework.request_reader.get_correlation_id(request)
        cf_logging.framework.context.set('correlation_id', correlation_id, request)
        cf_logging.framework.context.set('request_started_at', datetime.utcnow(), request)
        return wrapped(request)

    return _wrapper


def after_request(wrapped):
    """ Use as decorator on Sanic after_request handler
    Creates info log record per request
    """

    @wraps(wrapped)
    def _wrapper(request, response):
        cf_logging.framework.context.set('response_sent_at', datetime.utcnow(), request)
        extra = {REQUEST_KEY: request, RESPONSE_KEY: response}
        logging.getLogger('cf.sanic.logger').info('', extra=extra)
        return wrapped(request, response)

    return _wrapper


def init(app, level=defaults.DEFAULT_LOGGING_LEVEL, custom_framework=None):
    """ Initializes logging in JSON format.

    Adds before and after request handlers to the `app` object to enable request info log.
    :param app: - Flask application object
    :param level: - valid log level from standard logging package (optional)
    :param custom_framework: - `Framework` instance - use in case you need
        to change request processing behaviour for example to customize context storage
    """
    if not isinstance(app, Sanic):
        raise TypeError('application should be instance of Sanic')

    framework = custom_framework or \
                Framework(
                    SANIC_FRAMEWORK_NAME,
                    SanicContext(),
                    SanicRequestReader(),
                    SanicResponseReader()
                )

    cf_logging.init(framework, level)

    @app.middleware('request')
    @before_request
    def _before_request(request):  # pylint: disable=unused-argument
        pass

    @app.middleware('response')
    @after_request
    def _after_request(request, response):  # pylint: disable=unused-argument
        pass
