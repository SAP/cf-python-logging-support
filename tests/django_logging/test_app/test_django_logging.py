""" Module that tests the integration of cf_logging with Django """
import sys
import os
import pytest

from django.test import Client
from django.conf.urls import url
from django.conf import settings

from sap import cf_logging
from sap.cf_logging import django_logging
from tests.log_schemas import WEB_LOG_SCHEMA
from tests.common_test_params import (
    v_str, get_web_record_header_fixtures
)
from tests.util import (
    check_log_record,
    enable_sensitive_fields_logging,
    config_logger
)

from tests.django_logging.test_app.views import UserLoggingView


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.django_logging.test_app.settings'


@pytest.fixture(autouse=True)
def before_each():
    """ enable all fields to be logged """
    enable_sensitive_fields_logging()
    yield


FIXTURE = get_web_record_header_fixtures()

@pytest.mark.parametrize('headers, expected', FIXTURE)
def test_django_request_log(headers, expected):
    """ That the expected records are logged by the logging library """
    _set_up_django_logging()
    _check_django_request_log(headers, expected)


def test_web_log():
    """ That the custom properties are logged """
    _user_logging({}, {'myproperty': 'myval'}, {'myproperty': v_str('myval')})


def test_correlation_id():
    """ Test the correlation id is logged when coming from the headers """
    _user_logging(
        {'X-CorrelationID': '298ebf9d-be1d-11e7-88ff-2c44fd152860'},
        {},
        {'correlation_id': v_str('298ebf9d-be1d-11e7-88ff-2c44fd152860')},
        True
    )


def test_missing_request():
    """ That the correlation id is missing when the request is missing """
    _user_logging(
        {'X-CorrelationID': '298ebf9d-be1d-11e7-88ff-2c44fd152860'},
        {},
        {'correlation_id': v_str('-')},
        False
    )

def test_custom_fields_set():
    """ Test custom fields are set up """
    _set_up_django_logging()
    assert 'cf1' in cf_logging.FRAMEWORK.custom_fields.keys()

def _check_django_request_log(headers, expected):
    _, stream = config_logger('cf.django.logger')

    client = Client()
    _check_expected_response(client.get('/test/path', **headers), body='Hello test!')
    assert check_log_record(stream, WEB_LOG_SCHEMA, expected) == {}


# Helper functions
def _set_up_django_logging():
    cf_logging._SETUP_DONE = False # pylint: disable=protected-access
    django_logging.init(custom_fields={'cf1': None})


def _check_expected_response(response, status_code=200, body='ok'):
    assert response.status_code == status_code
    if body is not None:
        assert response.content.decode() == body


def _user_logging(headers, extra, expected, provide_request=False):
    sys.modules[settings.ROOT_URLCONF].urlpatterns.append(
        url('^test/user/logging$', UserLoggingView.as_view(provide_request=provide_request),
            {'extra': extra, 'expected': expected}))


    _set_up_django_logging()
    client = Client()
    _check_expected_response(client.get('/test/user/logging', **headers))
