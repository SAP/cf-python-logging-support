""" Test parameters common for Flask and Sanic """
import base64
import sys
from tests.schema_util import string as v_str
from tests.schema_util import num as v_num

if sys.version_info[0] == 3:
    def _bytes(arg):
        return bytes(arg, 'ascii')
else:
    def _bytes(arg):
        return bytes(arg)


def get_web_record_header_fixtures():
    """ returns: list of tuples (headers, expectation) """
    test_cases = [
        ({}, {
            'remote_user': v_str('-'),
            'method': v_str('GET'),
            'response_status': v_num(val=200),
            'response_content_type': v_str('text/plain'),
            'request': v_str('/test/path')})
    ]
    for header in ['X-Correlation-ID', 'X-CorrelationID', 'X-Request-ID', 'X-Vcap-Request-Id']:
        test_cases.append(({header: '298ebf9d-be1d-11e7-88ff-2c44fd152864'},
                           {'correlation_id': v_str('298ebf9d-be1d-11e7-88ff-2c44fd152864')}))

    return test_cases


def auth_basic(user, passwd):
    """ generates basic authentication header content """
    return 'Basic ' + base64.b64encode(_bytes(user + ':' + passwd)).decode('ascii')
