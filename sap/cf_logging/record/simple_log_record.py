""" Module SimpleLogRecord """
import logging
import traceback

from datetime import datetime
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.record import application_info
from sap.cf_logging.record import util

from sap.cf_logging.formatters.stacktrace_formatter import format_stacktrace

_SKIP_ATTRIBUTES = ["type", "written_at", "written_ts", "correlation_id", "remote_user", "referer",
                    "x_forwarded_for", "protocol", "method", "remote_ip", "request_size_b",
                    "remote_host", "remote_port", "request_received_at", "direction",
                    "response_time_ms", "response_status", "response_size_b",
                    "response_content_type", "response_sent_at", REQUEST_KEY, RESPONSE_KEY]


class SimpleLogRecord(logging.LogRecord):
    """ SimpleLogRecord class holds data for user logged messages """

    # pylint: disable=too-many-arguments,too-many-locals

    def __init__(self, extra, framework, *args, **kwargs):
        super(SimpleLogRecord, self).__init__(*args, **kwargs)

        utcnow = datetime.utcnow()
        self.written_at = util.iso_time_format(utcnow)
        self.written_ts = util.epoch_nano_second(utcnow)

        request = extra[REQUEST_KEY] if extra and REQUEST_KEY in extra else None

        self.correlation_id = framework.context.get_correlation_id(request) or defaults.UNKNOWN

        self.custom_fields = {}
        for key, value in framework.custom_fields.items():
            if extra and key in extra:
                if extra[key] is not None:
                    self.custom_fields[key] = extra[key]
            elif value is not None:
                self.custom_fields[key] = value

        self.extra = dict((key, value) for key, value in extra.items()
                          if key not in _SKIP_ATTRIBUTES and
                          key not in framework.custom_fields.keys()) if extra else {}
        for key, value in self.extra.items():
            setattr(self, key, value)

    def format_cf_attributes(self):
        """ Add common and Cloud Foundry environment specific attributes """
        record = {
            'component_id': application_info.COMPONENT_ID,
            'component_name': application_info.COMPONENT_NAME,
            'component_instance': application_info.COMPONENT_INSTANCE,
            'space_id': application_info.SPACE_ID,
            'space_name': application_info.SPACE_NAME,
            'container_id': application_info.CONTAINER_ID,
            'component_type': application_info.COMPONENT_TYPE,
            'written_at': self.written_at,
            'written_ts': self.written_ts,
            'correlation_id': self.correlation_id,
            'layer': application_info.LAYER
        }
        return record

    def format(self):
        """ Returns a dict record with properties to be logged """
        record = self.format_cf_attributes()
        record.update({
            'type': 'log',
            'logger': self.name,
            'thread': self.threadName,
            'level': self.levelname,
            'line_no': self.lineno,
            'msg': self.getMessage(),
        })

        if self.levelno == logging.ERROR and self.exc_info:
            stacktrace = ''.join(traceback.format_exception(*self.exc_info))
            record['stacktrace'] = format_stacktrace(stacktrace)

        record.update(self.extra)
        if len(self.custom_fields) > 0:
            record.update(self._format_custom_fields())
        return record

    def _format_custom_fields(self):
        res = {"#cf": {"string": []}}
        for i, (key, value) in enumerate(self.custom_fields.items()):
            res['#cf']['string'].append(
                {"k": str(key), "v": str(value), "i": i}
            )
        return res
