""" Module for the JsonFormatter """
import json
import logging
import sys

if sys.version_info[0] == 3:
    def _encode(obj):
        return json.dumps(obj)
else:
    def _encode(obj):
        return unicode(json.dumps(obj))  # pylint: disable=undefined-variable


class JsonFormatter(logging.Formatter):
    """
    Formatter for non-web application log
    """

    def format(self, record):
        """ Format the log record into a JSON object """
        if hasattr(record, 'format'):
            return _encode(record.format())
        return _encode(record.__dict__)
