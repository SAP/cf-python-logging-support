""" Module that tests the integration of cf_logging with Falcon """
import logging
import pytest
import falcon
from falcon import testing
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from sap import cf_logging
from sap.cf_logging import falcon_logging
from sap.cf_logging.core.constants import REQUEST_KEY
from tests.log_schemas import WEB_LOG_SCHEMA, JOB_LOG_SCHEMA
from tests.common_test_params import (
    v_str, auth_basic, get_web_record_header_fixtures
)
from tests.util import (
    check_log_record,
    config_logger,
    enable_sensitive_fields_logging
)


# pylint: disable=protected-access, missing-docstring,too-few-public-methods

@pytest.fixture(autouse=True)
def before_each():
    """ enable all fields to be logged """
    enable_sensitive_fields_logging()
    yield


@pytest.mark.xfail(raises=TypeError, strict=True)
def test_falcon_requires_valid_app():
    """ Test the init api expects a valid app """
    falcon_logging.init({})


FIXTURE = get_web_record_header_fixtures()

class TestResource:
    def on_get(self, req, resp): # pylint: disable=unused-argument,no-self-use
        resp.set_header('Content-Type', 'text/plain')
        resp.status = falcon.HTTP_200
        resp.body = 'ok'


@pytest.mark.parametrize('headers, expected', FIXTURE)
def test_falcon_request_log(headers, expected):
    """ That the expected records are logged by the logging library """
    app = falcon.API(middleware=falcon_logging.LoggingMiddleware())
    app.add_route('/test/path', TestResource())

    _set_up_falcon_logging(app)
    _check_falcon_request_log(app, headers, expected)


class User(object):  # pylint: disable=useless-object-inheritance
    def __init__(self, key, name):
        self.key = key
        self.name = name

@pytest.mark.parametrize('user', [
    User(None, 'user'),
    User('custom_username_key', 'new_user')
])
def test_falcon_request_logs_user(user):
    user_dict = dict([(user.key or 'username', user.name)])
    basic_auth = BasicAuthBackend(lambda username, password: user_dict)
    app = falcon.API(middleware=[
        falcon_logging.LoggingMiddleware(),
        FalconAuthMiddleware(basic_auth)
    ])
    app.add_route('/test/path', TestResource())

    args = [app, user.key] if user.key else [app]
    _set_up_falcon_logging(*args)

    expected = {'remote_user': v_str(user.name)}
    _check_falcon_request_log(app, {'Authorization': str(auth_basic(user.name, 'pass'))}, expected)


def _check_falcon_request_log(app, headers, expected):
    _, stream = config_logger('cf.falcon.logger')

    client = testing.TestClient(app)
    _check_expected_response(
        client.simulate_get('/test/path', headers=headers))
    assert check_log_record(stream, WEB_LOG_SCHEMA, expected) == {}


def test_web_log():
    """ That the custom properties are logged """
    _user_logging({}, {'myprop': 'myval'}, {'myprop': v_str('myval')})

def test_logging_without_request():
    """ Test logger is usable in non request context """
    app = falcon.API()
    _set_up_falcon_logging(app)
    cf_logging.FRAMEWORK.context.set_correlation_id('value')

    logger, stream = config_logger('main.logger')
    logger.info('works')
    assert check_log_record(stream, JOB_LOG_SCHEMA, {'msg': v_str('works')}) == {}


def test_correlation_id():
    """ Test the correlation id is logged when coming from the headers """
    _user_logging(
        {'X-Correlation-ID': '298ebf9d-be1d-11e7-88ff-2c44fd152860'},
        {},
        {'correlation_id': v_str('298ebf9d-be1d-11e7-88ff-2c44fd152860')}
    )

def test_custom_fields_set():
    """ Test custom fields are set up """
    app = falcon.API()
    _set_up_falcon_logging(app)
    assert 'cf1' in cf_logging.FRAMEWORK.custom_fields.keys()

# Helper functions
def _set_up_falcon_logging(app, *args):
    cf_logging._SETUP_DONE = False
    falcon_logging.init(app, logging.DEBUG, *args, custom_fields={'cf1': None})


class UserResourceRoute(object):  # pylint: disable=useless-object-inheritance
    def __init__(self, extra, expected):
        self.extra = extra
        self.expected = expected
        self.logger, self.stream = config_logger('user.logging')

    def on_get(self, req, resp):
        self.extra.update({REQUEST_KEY: req})
        self.logger.log(logging.INFO, 'in route headers', extra=self.extra)
        assert check_log_record(self.stream, JOB_LOG_SCHEMA, self.expected) == {}

        resp.set_header('Content-Type', 'text/plain')
        resp.status = falcon.HTTP_200
        resp.body = 'ok'


def _user_logging(headers, extra, expected):
    app = falcon.API(middleware=[
        falcon_logging.LoggingMiddleware()
    ])
    app.add_route('/test/user/logging', UserResourceRoute(extra, expected))
    _set_up_falcon_logging(app)
    client = testing.TestClient(app)
    _check_expected_response(client.simulate_get('/test/user/logging',
                                                 headers=headers))


def _check_expected_response(response, status_code=200, body='ok'):
    assert response.status_code == status_code
    if body is not None:
        assert response.text == body
