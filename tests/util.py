""" Module for common functions """
import io
import logging
import json
import os
from json_validator.validator import JsonValidator
from sap.cf_logging.formatters.json_formatter import JsonFormatter
from sap.cf_logging.core.constants import \
    LOG_SENSITIVE_CONNECTION_DATA, LOG_REMOTE_USER, LOG_REFERER

from tests.schema_util import extend


def check_log_record(stream, schema, expected):
    """ Using the JsonValidator check that the data in the stream
        matches the expected output
    """
    log_json = stream.getvalue()
    log_object = json.JSONDecoder().decode(log_json)
    expected_json = extend(schema, expected)
    _, error = JsonValidator(expected_json).validate(log_object)
    print('----------------------------------------------->')
    print(log_json)
    print('<-----------------------------------------------')
    return error


def config_logger(logger_name):
    """ Function to configure a JSONLogger and print the output into a stream"""
    stream = io.StringIO()
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setFormatter(JsonFormatter())
    logger = logging.getLogger(logger_name)
    logger.addHandler(stream_handler)
    return logger, stream

def enable_sensitive_fields_logging():
    """ sets a few logging related env vars """
    os.environ[LOG_SENSITIVE_CONNECTION_DATA] = 'true'
    os.environ[LOG_REMOTE_USER] = 'true'
    os.environ[LOG_REFERER] = 'true'
