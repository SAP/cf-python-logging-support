""" Module framework """
import sys
from sap.cf_logging.core.context import Context
from sap.cf_logging.core.request_reader import RequestReader
from sap.cf_logging.core.response_reader import ResponseReader

if sys.version_info[0] == 3:
    _STRClass = str
else:
    _STRClass = basestring  # pylint: disable=undefined-variable,invalid-name


def _check_instance(obj, clazz):
    if not isinstance(obj, clazz):
        raise TypeError('Provided object is not valid {}'.format(clazz.__name__))


class Framework(object):
    """ Framework class holds Context, RequestReader, ResponseReader """

    def __init__(self, name, context, request_reader, response_reader):
        if not name or not isinstance(name, _STRClass):
            raise TypeError('Provided name is not valid string')
        _check_instance(context, Context)
        _check_instance(request_reader, RequestReader)
        _check_instance(response_reader, ResponseReader)
        self._name = name
        self._context = context
        self._request_reader = request_reader
        self._response_reader = response_reader

    @property
    def context(self):
        """ Get Context """
        return self._context

    @property
    def request_reader(self):
        """ Get RequestReader """
        return self._request_reader

    @property
    def response_reader(self):
        """ Get Response Reader """
        return self._response_reader
