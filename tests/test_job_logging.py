""" Module to test the cf_logging library """
import logging
from json import JSONDecoder
import pytest
from json_validator.validator import JsonValidator
from sap import cf_logging
from tests.log_schemas import JOB_LOG_SCHEMA
from tests.util import config_root_logger

# pylint: disable=protected-access


@pytest.fixture(autouse=True)
def before_each():
    """ reset logging framework """
    cf_logging._SETUP_DONE = False


def test_log_in_expected_format():
    """ Test the cf_logger as a standalone """
    cf_logging.init(level=logging.DEBUG)
    logger, stream = config_root_logger('cli.test')
    logger.info('hi')
    log_json = JSONDecoder().decode(stream.getvalue())
    _, error = JsonValidator(JOB_LOG_SCHEMA).validate(log_json)

    assert error == {}


def test_set_correlation_id():
    """ Test setting correlation_id """
    correlation_id = '1234'
    cf_logging.init(level=logging.DEBUG)
    cf_logging.FRAMEWORK.context.set_correlation_id(correlation_id)

    logger, stream = config_root_logger('cli.test')
    logger.info('hi')

    log_json = JSONDecoder().decode(stream.getvalue())
    _, error = JsonValidator(JOB_LOG_SCHEMA).validate(log_json)

    assert error == {}
    assert log_json['correlation_id'] == correlation_id
    assert cf_logging.FRAMEWORK.context.get_correlation_id() == correlation_id
