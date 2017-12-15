""" Module that holds the RequestWebRecord class """
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.record import util
from sap.cf_logging.record.simple_log_record import SimpleLogRecord


PROPS = ['type', 'direction', 'remote_user', 'request', 'referer',
         'x_forwarded_for', 'protocol', 'method', 'remote_ip',
         'request_size_b', 'remote_host', 'remote_port', 'request_received_at',
         'response_sent_at', 'response_time_ms', 'response_status',
         'response_size_b', 'response_content_type']

# pylint: disable=too-many-instance-attributes


class RequestWebRecord(SimpleLogRecord):
    """ RequestWebRecord class holds request/response log data
        It is used in the formatter class
    """

    # pylint: disable=too-many-locals
    def __init__(self, extra, framework, *args, **kwargs):

        super(RequestWebRecord, self).__init__(extra, framework, *args, **kwargs)

        context = framework.context
        request_reader = framework.request_reader
        response_reader = framework.response_reader

        request = extra[REQUEST_KEY]
        response = extra[RESPONSE_KEY]

        props = dict((key, value) for key, value in extra.items()
                     if key not in [RESPONSE_KEY, REQUEST_KEY])
        for key, value in props.items():
            setattr(self, key, value)

        length = request_reader.get_content_length(request)
        remote_ip = request_reader.get_remote_ip(request)

        self.type = 'request'
        self.direction = 'IN'
        self.remote_user = request_reader.get_remote_user(request)
        self.request = request_reader.get_path(request)
        self.referer = request_reader.get_http_header(
            request, 'referer', defaults.UNKNOWN)
        self.x_forwarded_for = request_reader.get_http_header(
            request, 'x-forwarded-for', defaults.UNKNOWN)
        self.protocol = request_reader.get_protocol(request)
        self.method = request_reader.get_method(request)
        self.remote_ip = remote_ip
        self.request_size_b = util.parse_int(length, -1)
        self.remote_host = remote_ip
        self.remote_port = request_reader.get_remote_port(
            request) or defaults.UNKNOWN

        request_start = context.get(
            'request_started_at', request) or defaults.UNIX_EPOCH
        self.request_received_at = util.iso_time_format(request_start)

        # response related
        response_sent_at = context.get(
            'response_sent_at', request) or defaults.UNIX_EPOCH
        self.response_sent_at = util.iso_time_format(response_sent_at)
        self.response_time_ms = util.time_delta_ms(
            request_start, response_sent_at)

        self.response_status = util.parse_int(
            response_reader.get_status_code(response), defaults.STATUS)
        self.response_size_b = util.parse_int(
            response_reader.get_response_size(response), defaults.RESPONSE_SIZE_B)
        self.response_content_type = response_reader.get_content_type(response)

    def format(self):
        record = super(RequestWebRecord, self).format_cf_attributes()
        request_properties = dict(
            (key, value) for key, value in self.__dict__.items() if key in PROPS)
        record.update(request_properties)
        return record
