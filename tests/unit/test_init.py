""" Tests for cf_logging.init """
import logging
import pytest
from sap import cf_logging

from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.record.request_log_record import RequestWebRecord
from sap.cf_logging.record.simple_log_record import SimpleLogRecord


# pylint: disable=protected-access

@pytest.mark.xfail(raises=RuntimeError, reason='cf_logging.init can be called once', strict=True)
def test_init_called_twice(mocker):
    """ test cf_logging.init can be called only once """
    framework = mocker.Mock(Framework)
    cf_logging._SETUP_DONE = False
    cf_logging.init(framework, level=logging.DEBUG)
    cf_logging.init(framework, level=logging.DEBUG)


@pytest.mark.xfail(raises=TypeError, reason='', strict=True)
def test_init_incorrect_framework():
    """ test cf_logging.init fails for invalid framework """
    cf_logging._SETUP_DONE = False
    cf_logging.init({})


def _make_record(extra):
    cf_logger = cf_logging.CfLogger('mylogger')
    return cf_logger.makeRecord('', '', '', '', '', '', '', '', extra=extra)


def test_init_cf_logger_simple_log(mocker):
    """ tests CfLogger creates SimpleLogRecord if extra is incomplete """
    framework = mocker.Mock(Framework)
    mocker.patch.object(framework, 'custom_fields', return_value=None)
    cf_logging.init(framework)
    assert isinstance(_make_record(extra={}), SimpleLogRecord)
    assert isinstance(_make_record(extra={REQUEST_KEY: {}}), SimpleLogRecord)
    assert isinstance(_make_record(extra={RESPONSE_KEY: {}}), SimpleLogRecord)


def test_init_cf_logger_web_log(mocker):
    """ tests CfLogger creates SimpleLogRecord if extra contains request and response """
    mocker.patch.object(RequestWebRecord, '__init__', lambda *a, **kwa: None)
    record = _make_record(extra={REQUEST_KEY: {}, RESPONSE_KEY: {}})
    assert isinstance(record, RequestWebRecord)
