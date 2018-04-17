""" Tests json log formatting """
import json
import logging
from sap.cf_logging.record.simple_log_record import SimpleLogRecord
from sap.cf_logging.formatters.json_formatter import JsonFormatter

lvl, fn, lno, func, exc_info = logging.INFO, "(unknown file)", 0, "(unknown function)", None
formatter = JsonFormatter()


def test_unknown_records_format():
    """ test unknown log records will be delegated to logging.Formatter """
    log_record = logging.LogRecord('name', lvl, fn, lno, 'msg', [], exc_info)
    assert formatter.format(log_record) == 'msg'


def test_non_json_serializable():
    """ test json formatter handles non JSON serializable object """
    class MyClass(object): pass
    extra = { 'cls': MyClass() } 
    log_record = SimpleLogRecord(extra, None, 'name', lvl, fn, lno, 'msg', [], exc_info)
    record_object = json.loads(formatter.format(log_record))
    assert record_object.get('cls') is not None
    assert 'MyClass' in record_object.get('cls')
