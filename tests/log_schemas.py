""" Log JSON schemas according to sonic182-json-validator
to be used for validation of real log records """
import tests.schema_util as u

CF_ATTRIBUTES_SCHEMA = {
    'layer': u.string(r'^python$'),
    'component_id': u.string(u.TEXT),
    'component_name': u.string(u.TEXT),
    'component_instance': u.pos_num(),
    'space_id': u.string(u.TEXT),
    'space_name': u.string(u.TEXT),
    'container_id': u.string(u.TEXT),
    'component_type': u.string(u.TEXT)
}

JOB_LOG_SCHEMA = u.extend(CF_ATTRIBUTES_SCHEMA, {
    'type': {
        'in': ['log'],
        'in_error': 'Invalid "type" property'
    },
    'correlation_id': u.string(r'([a-z\d]+-?)*'),
    'logger': u.string(u.WORD),
    'thread': u.string(u.WORD),
    'level': u.enum(u.LEVEL),
    'written_at': u.iso_datetime(),
    'written_ts': u.pos_num(),
    'msg': u.string(u.WORD),
    'component_type': u.string(r'^application$'),
})

CUST_FIELD_SCHEMA = u.extend(JOB_LOG_SCHEMA, {
    '#cf': {
        'type': dict,
        'properties': {
            'string': {'type' : list, 'items': {
                'type': dict,
                'properties': {
                    'v': u.string(u.WORD),
                    'k': u.string(u.WORD),
                    'i': u.pos_num()
                }
            }}
        }
    }
})

WEB_LOG_SCHEMA = u.extend(CF_ATTRIBUTES_SCHEMA, {
    'type': u.string('^request$'),
    'written_at': u.iso_datetime(),
    'written_ts': u.pos_num(),
    'correlation_id': u.string(r'.*'),
    # 'correlation_id' : u.string(r'[a-z|\d+-|\d]+'),
    'remote_user': u.string(u.TEXT),
    'request': u.string(r'^/.*'),
    'referer': u.string(u.TEXT),
    'x_forwarded_for': u.string(u.TEXT),
    'protocol': u.string(u.TEXT),
    'method': u.string(r'^GET$'),
    'remote_ip': u.string(u.IP),
    'request_size_b': u.num(),
    'remote_host': u.string(u.HOST_NAME),
    'remote_port': u.string(u.STRING_NUM),
    'request_received_at': u.iso_datetime(),
    'direction': u.string(r'IN'),
    'response_time_ms': u.pos_num(),
    'response_status': u.pos_num(),
    'response_size_b': u.num(),
    'response_content_type': u.string(r'^text/.*'),
    'response_sent_at': u.iso_datetime()
})
