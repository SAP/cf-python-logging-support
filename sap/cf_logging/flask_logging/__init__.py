""" Flask logging support package
- Configures standard logging package to produce JSON
- Produces info request log entry per request
"""
import logging
from datetime import datetime
from functools import wraps
import flask
from flask import request

from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.flask_logging.context import FlaskContext
from sap.cf_logging.flask_logging.request_reader import FlaskRequestReader
from sap.cf_logging.flask_logging.response_reader import FlaskResponseReader

FLASK_FRAMEWORK_NAME = 'flask.framework'


def before_request(wrapped):
    """ Use as a decorator on Flask before_request handler
    Handles correlation_id by setting it in the context for log records
    """
    @wraps(wrapped)
    def _wrapper():
        framework = cf_logging.framework
        cid = framework.request_reader.get_correlation_id(request)
        framework.context.set('correlation_id', cid, request)
        framework.context.set('request_started_at', datetime.utcnow(), request)
        return wrapped()
    return _wrapper


def after_request(wrapped):
    """ Use as a decorator on Flask after_request handler
    Creates info log record per request
    """
    @wraps(wrapped)
    def _wrapper(response):
        cf_logging.framework.context.set(
            'response_sent_at', datetime.utcnow(), request)
        extra = {REQUEST_KEY: request, RESPONSE_KEY: response}
        logging.getLogger('cf.flask.logger').info('', extra=extra)
        return wrapped(response)
    return _wrapper


def init(app, level=defaults.DEFAULT_LOGGING_LEVEL):
    """ Initializes logging in JSON format.

    Adds before and after request handlers to `app` object to enable request info log.
    :param app: - Flask application object
    :param level: - valid log level from standard logging package (optional)
    """
    if not isinstance(app, flask.Flask):
        raise TypeError('application should be instance of Flask')

    _init_framework(level)

    @app.before_request
    @before_request
    def _app_before_request():
        pass

    @app.after_request
    @after_request
    def _app_after_request(response):
        return response


def _init_framework(level):
    logging.getLogger('werkzeug').disabled = True

    framework = Framework(FLASK_FRAMEWORK_NAME,
                          FlaskContext(), FlaskRequestReader(), FlaskResponseReader())
    cf_logging.init(framework, level)
