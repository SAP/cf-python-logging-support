"""Module to test the cf_logging library"""
import uuid
import logging
import time
import threading
from json import JSONDecoder
import pytest
from json_validator.validator import JsonValidator
from sap import cf_logging
from tests.log_schemas import JOB_LOG_SCHEMA
from tests.util import config_logger

# pylint: disable=protected-access

@pytest.fixture(autouse=True)
def before_each():
    """Reset logging framework and clear log handlers"""
    cf_logging._SETUP_DONE = False
    logging.getLogger().handlers = []

@pytest.mark.parametrize('log_callback', [
    lambda logger, msg: logger.debug('message: %s', msg),
    lambda logger, msg: logger.info('message: %s', msg),
    lambda logger, msg: logger.warning('message: %s', msg),
    lambda logger, msg: logger.error('message: %s', msg),
    lambda logger, msg: logger.critical('message: %s', msg)
])
def test_log_in_expected_format(log_callback):
    """Test the cf_logger as a standalone"""
    cf_logging.init(level=logging.DEBUG)
    logger, stream = config_logger('cli.test')
    log_callback(logger, 'hi')
    log_json = JSONDecoder().decode(stream.getvalue())
    _, error = JsonValidator(JOB_LOG_SCHEMA).validate(log_json)

    assert error == {}
    assert not check_duplicates(stream.getvalue())

def test_set_correlation_id():
    """Test setting correlation_id"""
    correlation_id = '1234'
    cf_logging.init(level=logging.DEBUG)
    cf_logging.FRAMEWORK.context.set_correlation_id(correlation_id)

    logger, stream = config_logger('cli.test')
    logger.info('hi')

    log_json = JSONDecoder().decode(stream.getvalue())
    _, error = JsonValidator(JOB_LOG_SCHEMA).validate(log_json)

    assert error == {}
    assert log_json['correlation_id'] == correlation_id
    assert cf_logging.FRAMEWORK.context.get_correlation_id() == correlation_id
    assert not check_duplicates(stream.getvalue())

def test_exception_stacktrace():
    """Test exception stacktrace is logged"""
    cf_logging.init(level=logging.DEBUG)
    logger, stream = config_logger('cli.test')

    try:
        return 1 / 0
    except ZeroDivisionError:
        logger.exception('zero division error')
        log_json = JSONDecoder().decode(stream.getvalue())
        _, error = JsonValidator(JOB_LOG_SCHEMA).validate(log_json)

        assert error == {}
        assert 'ZeroDivisionError' in str(log_json['stacktrace'])
        assert 'ZeroDivisionError' in log_json["msg"]
        assert not check_duplicates(stream.getvalue())

def test_exception_stacktrace_info_level():
    """Test exception stacktrace is logged at info level"""
    cf_logging.init(level=logging.DEBUG)
    logger, stream = config_logger('cli.test')

    try:
        return 1 / 0
    except ZeroDivisionError as exc:
        logger.info('zero division error', exc_info=exc)
        log_json = JSONDecoder().decode(stream.getvalue())
        _, error = JsonValidator(JOB_LOG_SCHEMA).validate(log_json)

        assert error == {}
        assert 'ZeroDivisionError' in str(log_json['stacktrace'])
        assert 'ZeroDivisionError' in log_json["msg"]
        assert not check_duplicates(stream.getvalue())

def test_custom_fields_set():
    """Test custom fields are set up"""
    cf_logging.init(level=logging.DEBUG, custom_fields={'cf1': None})
    assert 'cf1' in cf_logging.FRAMEWORK.custom_fields.keys()
    logger, stream = config_logger('cli.test')
    logger.info('hi')
    assert not check_duplicates(stream.getvalue())

def test_thread_safety():
    """Test context keeps separate correlation ID per thread"""
    class _SampleThread(threading.Thread):
        def __init__(self):
            super().__init__()
            self.correlation_id = str(uuid.uuid1())
            self.read_correlation_id = ''

        def run(self):
            cf_logging.FRAMEWORK.context.set_correlation_id(self.correlation_id)
            time.sleep(0.1)
            self.read_correlation_id = cf_logging.FRAMEWORK.context.get_correlation_id()

    cf_logging.init(level=logging.DEBUG)

    thread_one = _SampleThread()
    thread_two = _SampleThread()

    thread_one.start()
    thread_two.start()

    thread_one.join()
    thread_two.join()

    assert thread_one.correlation_id == thread_one.read_correlation_id
    assert thread_two.correlation_id == thread_two.read_correlation_id
    logger, stream = config_logger('cli.test')
    logger.info('hi')
    assert not check_duplicates(stream.getvalue())

def check_duplicates(log_stream):
    """Check for duplicate log records in the log stream"""
    log_lines = log_stream.splitlines()
    seen_logs = set()
    for line in log_lines:
        if line in seen_logs:
            return True
        seen_logs.add(line)
    return False
