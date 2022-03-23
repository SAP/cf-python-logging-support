""" Tests json log formatting """
import json
import logging
from sap.cf_logging.job_logging.framework import JobFramework
from sap.cf_logging.record.simple_log_record import SimpleLogRecord
from sap.cf_logging.formatters.json_formatter import JsonFormatter


LEVEL, FILE, LINE, EXC_INFO = logging.INFO, "(unknown file)", 0, None
FORMATTER = JsonFormatter()


def test_unknown_records_format():
    """ test unknown log records will be delegated to logging.Formatter """
    log_record = logging.LogRecord('name', LEVEL, FILE, LINE, 'msg', [], EXC_INFO)
    assert FORMATTER.format(log_record) == 'msg'


def test_non_json_serializable():
    """ test json formatter handles non JSON serializable object """
    class _MyClass(object): # pylint: disable=too-few-public-methods,useless-object-inheritance
        pass

    extra = {'cls': _MyClass()}
    framework = JobFramework()
    log_record = SimpleLogRecord(extra, framework, 'name', LEVEL, FILE, LINE, 'msg', [], EXC_INFO)
    record_object = json.loads(FORMATTER.format(log_record))
    assert record_object.get('cls') is not None
    assert 'MyClass' in record_object.get('cls')

def test_stacktrace_is_added_to_msg_field():
    """
    Tests that JSONFormatter adds stracktrace to msg field. The stacktrace field
    is no longer rendered in Kibana, see https://github.com/SAP/cf-python-logging-support/issues/45
    for related report.
    """
    # Generate exception for the test
    try:
        raise ValueError("Dummy Exception")
    except ValueError as e:
        exc_info = (type(e), e, e.__traceback__)

    framework = JobFramework()
    extra = {}

    log_record = SimpleLogRecord(extra, framework, 'name', logging.ERROR, FILE, LINE, 'Error found!', [], exc_info)
    record_object = json.loads(FORMATTER.format(log_record))
    assert "Dummy Exception" in "".join(record_object["stacktrace"])
    expected_msg = "Error found!"
    expected_msg += "\n"
    expected_msg += "\n".join(record_object["stacktrace"])
    assert record_object["msg"] == expected_msg
