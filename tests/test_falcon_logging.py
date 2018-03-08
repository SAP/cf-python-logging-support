""" Module that tests the integration of cf_logging with Falcon """
import logging
import pytest
import falcon
from falcon import testing
from sap import cf_logging
from sap.cf_logging import falcon_logging
from tests.log_schemas import WEB_LOG_SCHEMA, CLI_LOG_SCHEMA
from tests.common_test_params import (
    v_str, v_num, auth_basic, get_web_record_header_fixtures
)
from tests.util import check_log_record, config_root_logger


# pylint: disable=protected-access

@pytest.mark.xfail(raises=TypeError, strict=True)
def test_falcon_requires_valid_app():
    """ Test the init api expects a valid app """
    falcon_logging.init({})


FIXTURE = get_web_record_header_fixtures()
FIXTURE.append(({'Authorization': auth_basic('user', 'pass')},
                {'remote_user': v_str('user')}))


class TestResource:
    def on_get(self, req, resp):
        resp.set_header('Content-Type', 'text/plain')
        resp.status = falcon.HTTP_200
        resp.body = 'ok'


@pytest.mark.parametrize("headers, expected", FIXTURE)
def test_falcon_request_log(headers, expected):
    """ That the expected records are logged by the logging library """
    app = falcon.API(middleware=[
        falcon_logging.LoggingMiddleware()
    ])
    app.add_route('/test/path', TestResource())

    _set_up_falcon_logging(app)
    _, stream = config_root_logger('cf.falcon.logger')

    client = testing.TestClient(app)
    _check_expected_response(
        client.simulate_get('/test/path', headers=headers))
    assert check_log_record(stream, WEB_LOG_SCHEMA, expected) == {}


def test_web_log():
    """ That the custom properties are logged """
    _user_logging({}, {'myprop': 'myval'}, {'myprop': v_str('myval')})


def test_correlation_id():
    """ Test the correlation id is logged when coming from the headers """
    _user_logging(
        {'X-CorrelationID': '298ebf9d-be1d-11e7-88ff-2c44fd152860'},
        {},
        {'correlation_id': v_str('298ebf9d-be1d-11e7-88ff-2c44fd152860')}
    )


# Helper functions
def _set_up_falcon_logging(app, level=logging.DEBUG):
    cf_logging._setup_done = False
    falcon_logging.init(app, level)


class TestUserResource:

    def __init__(self, extra, expected):
        self.extra = extra
        self.expected = expected

    def on_get(self, req, resp):
        _, stream = config_root_logger('user.logging')
        req.log('in route headers', extra=self.extra)
        # logger.info('in route headers', extra=self.extra)
        assert check_log_record(stream, CLI_LOG_SCHEMA, self.expected) == {}

        resp.set_header('Content-Type', 'text/plain')
        resp.status = falcon.HTTP_200
        resp.body = 'ok'


def _user_logging(headers, extra, expected):
    app = falcon.API(middleware=[
        falcon_logging.LoggingMiddleware()
    ])
    app.add_route('/test/user/logging', TestUserResource(extra, expected))
    _set_up_falcon_logging(app)
    client = testing.TestClient(app)
    _check_expected_response(client.simulate_get('/test/user/logging',
                             headers=headers))


def _check_expected_response(response, status_code=200, body='ok'):
    assert response.status_code == status_code
    if body is not None:
        assert response.text == body
