""" Module that tests the integration of cf_logging with Sanic """
import logging
import pytest
import sanic
from sanic.response import text
from sap import cf_logging

from sap.cf_logging import sanic_logging
from tests.log_schemas import WEB_LOG_SCHEMA, JOB_LOG_SCHEMA
from tests.common_test_params import v_str, v_num, get_web_record_header_fixtures
from tests.schema_util import extend
from tests.util import (
    check_log_record,
    config_logger,
    enable_sensitive_fields_logging,
)


# pylint: disable=protected-access
@pytest.mark.xfail(raises=TypeError, strict=True)
def test_sanic_requires_valid_app():
    """ Test that the api requires a valid app to be passed in """
    sanic_logging.init({})


FIXTURE = get_web_record_header_fixtures()
FIXTURE.append(({'no-content-length': '1'}, {'response_size_b': v_num(-1)}))


@pytest.fixture(autouse=True)
def before_each():
    """ enable all fields to be logged """
    enable_sensitive_fields_logging()
    yield


@pytest.mark.parametrize("headers, expected", FIXTURE)
def test_sanic_request_log(headers, expected):
    """ Test that the JSON logs contain the expected properties based on the
        input.
    """
    app = sanic.Sanic('test cf_logging')

    @app.route('/test/path')
    async def _headers_route(request):
        if 'no-content-length' in request.headers:
            return text('ok', headers={'Content-Type': 'text/plain'})
        return text('ok', headers={'Content-Length': 2, 'Content-Type': 'text/plain'})

    _set_up_sanic_logging(app)
    _, stream = config_logger('cf.sanic.logger')

    client = app.test_client
    _check_expected_response(client.get(
        '/test/path', headers=headers)[1], 200, 'ok')
    assert check_log_record(stream, WEB_LOG_SCHEMA, expected) == {}


def test_web_log():
    """ Test that custom attributes are logged """
    _user_logging({}, {'myprop': 'myval'}, {'myprop': v_str('myval')}, False)


def test_missing_request():
    """ That the correlation ID when the request is missing """
    _user_logging({'X-CorrelationID': '298ebf9d-be1d-11e7-88ff-2c44fd152860'},
                  {},
                  {'correlation_id': v_str('-')},
                  False)


def test_logs_correlation_id():
    """ Test the setting of the correlation id based on the headers """
    _user_logging({'X-CorrelationID': '298ebf9d-be1d-11e7-88ff-2c44fd152860'},
                  {},
                  {'correlation_id': v_str(
                      '298ebf9d-be1d-11e7-88ff-2c44fd152860')},
                  True)

def test_custom_fields_set():
    """ Test custom fields are set up """
    app = sanic.Sanic('test cf_logging')
    _set_up_sanic_logging(app)
    assert 'cf1' in cf_logging.FRAMEWORK.custom_fields.keys()


# Helper functions
def _set_up_sanic_logging(app, level=logging.DEBUG):
    cf_logging._SETUP_DONE = False
    sanic_logging.init(app, level, custom_fields={'cf1': None})


def _user_logging(headers, extra, expected, provide_request=False):
    app = sanic.Sanic(__name__)

    @app.route('/test/user/logging')
    async def _logging_correlation_id_route(request):
        logger, stream = config_logger('user.logging')
        new_extra = extend(extra, {'request': request}) if provide_request else extra
        logger.info('in route headers', extra=new_extra)
        assert check_log_record(stream, JOB_LOG_SCHEMA, expected) == {}
        return text('ok')

    _set_up_sanic_logging(app)
    client = app.test_client
    _check_expected_response(client.get('/test/user/logging', headers=headers)[1])


def _check_expected_response(response, status_code=200, body=None):
    print(response.text)
    assert response.status == status_code

    if body is not None:
        assert response.text == body
