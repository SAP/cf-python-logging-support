""" Module for the JsonFormatter """
import json
import logging
import sys
from sap.cf_logging.record.simple_log_record import SimpleLogRecord

def _default_serializer(obj):
    return str(obj)

if sys.version_info[0] == 3:
    def _encode(obj):
        return json.dumps(obj, default=_default_serializer)
else:
    def _encode(obj):
        return unicode(json.dumps(obj, default=_default_serializer))  # pylint: disable=undefined-variable


class JsonFormatter(logging.Formatter):
    """
    Format application log in JSON format
    """

    def format(self, record):
        """ Format the known log records in JSON format """
        if isinstance(record, SimpleLogRecord):
            return _encode(record.format())
        return super(JsonFormatter, self).format(record)
