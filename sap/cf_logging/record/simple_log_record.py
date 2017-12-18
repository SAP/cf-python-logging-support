""" Module SimpleLogRecord """
import logging
from datetime import datetime
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.record import application_info
from sap.cf_logging.record import util

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

        correlation_id = None
        if framework is not None:
            correlation_id = framework.context.get('correlation_id', request)

        self.correlation_id = correlation_id or '-'

        self.extra = dict((key, value) for key, value in extra.items()
                          if key not in _SKIP_ATTRIBUTES) if extra else {}
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

        record.update(self.extra)
        return record
