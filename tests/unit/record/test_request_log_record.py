""" Test `RequestWebRecord` """
import logging
import os
import pytest
from sap.cf_logging import defaults
from sap.cf_logging.record.request_log_record import RequestWebRecord
from sap.cf_logging.core.context import Context
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.core.request_reader import RequestReader
from sap.cf_logging.core.response_reader import ResponseReader
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY

# pylint: disable=missing-docstring, invalid-name

FRAMEWORK = None

@pytest.fixture(autouse=True)
def before_each_setup_mocks(mocker):
    context = Context()
    mocker.patch.object(context, 'get', return_value=None)

    request_reader = RequestReader()

    request_reader.get_http_header = lambda self, key, default: 'some.host' \
        if key == 'x-forwarded-for' else 'referer'

    mocker.patch.object(request_reader, 'get_remote_user', return_value='user')
    mocker.patch.object(request_reader, 'get_protocol', return_value='http')
    mocker.patch.object(request_reader, 'get_content_length', return_value=0)
    mocker.patch.object(request_reader, 'get_remote_ip',
                        return_value='1.2.3.4')
    mocker.patch.object(request_reader, 'get_remote_port', return_value='1234')
    mocker.patch.object(request_reader, 'get_path', return_value='/test/path')
    mocker.patch.object(request_reader, 'get_method', return_value='GET')

    response_reader = ResponseReader()
    mocker.patch.object(response_reader, 'get_status_code', return_value='200')
    mocker.patch.object(response_reader, 'get_response_size', return_value=0)
    mocker.patch.object(response_reader, 'get_content_type',
                        return_value='text/plain')

    _clean_log_env_vars()

    global FRAMEWORK # pylint: disable=global-statement
    FRAMEWORK = Framework('name', context, request_reader, response_reader)
    yield


def test_hiding_sensitive_fields_by_default():
    log_record = RequestWebRecord({REQUEST_KEY: None, RESPONSE_KEY: None},
                                  FRAMEWORK, 'name', logging.DEBUG, 'pathname', 1, 'msg', [], None)

    _assert_sensitive_fields_redacted(log_record)
    assert log_record.remote_user == defaults.REDACTED
    assert log_record.referer == defaults.REDACTED


def test_logging_sensitive_connection_data():
    os.environ['LOG_SENSITIVE_CONNECTION_DATA'] = 'true'

    log_record = RequestWebRecord({REQUEST_KEY: None, RESPONSE_KEY: None},
                                  FRAMEWORK, 'name', logging.DEBUG, 'pathname', 1, 'msg', [], None)

    assert log_record.remote_ip == '1.2.3.4'
    assert log_record.remote_host == '1.2.3.4'
    assert log_record.remote_port == '1234'
    assert log_record.x_forwarded_for == 'some.host'
    assert log_record.remote_user == defaults.REDACTED
    assert log_record.referer == defaults.REDACTED


def test_logging_remote_user():
    os.environ['LOG_REMOTE_USER'] = 'true'

    log_record = RequestWebRecord({REQUEST_KEY: None, RESPONSE_KEY: None},
                                  FRAMEWORK, 'name', logging.DEBUG, 'pathname', 1, 'msg', [], None)

    _assert_sensitive_fields_redacted(log_record)
    assert log_record.remote_user == 'user'
    assert log_record.referer == defaults.REDACTED


def test_logging_referer():
    os.environ['LOG_REFERER'] = 'true'

    log_record = RequestWebRecord({REQUEST_KEY: None, RESPONSE_KEY: None},
                                  FRAMEWORK, 'name', logging.DEBUG, 'pathname', 1, 'msg', [], None)

    _assert_sensitive_fields_redacted(log_record)
    assert log_record.remote_user == defaults.REDACTED
    assert log_record.referer == 'referer'


def test_incorrect_env_var_value():
    os.environ['LOG_SENSITIVE_CONNECTION_DATA'] = 'false'
    os.environ['LOG_REMOTE_USER'] = 'some-string'
    os.environ['LOG_REFERER'] = ''

    log_record = RequestWebRecord({REQUEST_KEY: None, RESPONSE_KEY: None},
                                  FRAMEWORK, 'name', logging.DEBUG, 'pathname', 1, 'msg', [], None)

    _assert_sensitive_fields_redacted(log_record)
    assert log_record.remote_user == defaults.REDACTED
    assert log_record.referer == defaults.REDACTED


def _clean_log_env_vars():
    for key in ['LOG_SENSITIVE_CONNECTION_DATA', 'LOG_REMOTE_USER', 'LOG_REFERER']:
        if os.environ.get(key):
            del os.environ[key]


def _assert_sensitive_fields_redacted(log_record):
    assert log_record.remote_ip == defaults.REDACTED
    assert log_record.remote_host == defaults.REDACTED
    assert log_record.remote_port == defaults.REDACTED
    assert log_record.x_forwarded_for == defaults.REDACTED
