""" Module that tests the integration of cf_logging with Flask """
import logging
import pytest
from flask import Flask
from flask import Response
from sap import cf_logging
from sap.cf_logging import flask_logging
from tests.log_schemas import WEB_LOG_SCHEMA, JOB_LOG_SCHEMA, CUST_FIELD_SCHEMA
from tests.common_test_params import v_str, v_num, auth_basic, get_web_record_header_fixtures
from tests.util import (
    check_log_record,
    enable_sensitive_fields_logging,
    config_logger,
)


# pylint: disable=protected-access

@pytest.mark.xfail(raises=TypeError, strict=True)
def test_flask_requires_valid_app():
    """ Test the init api expects a valid app """
    flask_logging.init({})


FIXTURE = get_web_record_header_fixtures()
FIXTURE.append(({'Authorization': auth_basic('user', 'pass')},
                {'remote_user': v_str('user')}))
FIXTURE.append(({}, {'response_size_b': v_num(val=2)}))


@pytest.fixture(autouse=True)
def before_each():
    # pylint: disable=duplicate-code
    """ enable all fields to be logged """
    enable_sensitive_fields_logging()
    yield


@pytest.mark.parametrize("headers, expected", FIXTURE)
def test_flask_request_log(headers, expected):
    """ That the expected records are logged by the logging library """

    app = Flask(__name__)

    @app.route('/test/path')
    def _root():
        return Response('ok', mimetype='text/plain')

    _set_up_flask_logging(app)
    _, stream = config_logger('cf.flask.logger')

    client = app.test_client()
    _check_expected_response(client.get('/test/path', headers=headers))
    assert check_log_record(stream, WEB_LOG_SCHEMA, expected) == {}


def test_web_log():
    """ That the custom properties are logged """
    _user_logging({}, {'myprop': 'myval'}, {'myprop': v_str('myval')})


def test_correlation_id():
    """ Test the correlation id is logged when coming from the headers """
    _user_logging({'X-CorrelationID': '298ebf9d-be1d-11e7-88ff-2c44fd152860'},
                  {},
                  {'correlation_id': v_str('298ebf9d-be1d-11e7-88ff-2c44fd152860')})


def test_logging_without_request():
    """ Test logger is usable in non request context """
    app = Flask(__name__)
    _set_up_flask_logging(app)
    logger, stream = config_logger('main.logger')
    logger.info('works')
    assert check_log_record(stream, JOB_LOG_SCHEMA, {'msg': v_str('works')}) == {}

def test_custom_field_loggin():
    """ Test custom fields are generated """
    app = Flask(__name__)
    _set_up_flask_logging(app)
    logger, stream = config_logger('main.logger')
    logger.info('works', extra={'cf1': 'yes'})
    assert check_log_record(stream, CUST_FIELD_SCHEMA, {}) == {}

# Helper functions
def _set_up_flask_logging(app, level=logging.DEBUG):
    cf_logging._SETUP_DONE = False
    flask_logging.init(app, level, custom_fields={'cf1': None, 'cf2': None})


def _user_logging(headers, extra, expected):
    app = Flask(__name__)

    @app.route('/test/user/logging')
    def _logging_correlation_id_route():
        logger, stream = config_logger('user.logging')
        logger.info('in route headers', extra=extra)
        assert check_log_record(stream, JOB_LOG_SCHEMA, expected) == {}
        return Response('ok')

    _set_up_flask_logging(app)
    client = app.test_client()
    _check_expected_response(client.get('/test/user/logging', headers=headers))


def _check_expected_response(response, status_code=200, body='ok'):
    assert response.status_code == status_code
    if body is not None:
        assert response.get_data().decode() == body
