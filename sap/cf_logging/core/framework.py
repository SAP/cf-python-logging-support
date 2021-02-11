""" Module framework """
import sys
from sap.cf_logging.core.context import Context
from sap.cf_logging.core.request_reader import RequestReader
from sap.cf_logging.core.response_reader import ResponseReader


STR_CLASS = str if sys.version_info[0] == 3 else basestring # pylint: disable=undefined-variable


def _check_instance(obj, clazz):
    if not isinstance(obj, clazz):
        raise TypeError('Provided object is not valid {}'.format(clazz.__name__))


class Framework(object):  # pylint: disable=useless-object-inheritance
    """ Framework class holds Context, RequestReader, ResponseReader """

    # pylint: disable=too-many-arguments
    def __init__(self, name, context, request_reader, response_reader, custom_fields=None):
        if not name or not isinstance(name, STR_CLASS):
            raise TypeError('Provided name is not valid string')
        _check_instance(context, Context)
        _check_instance(request_reader, RequestReader)
        _check_instance(response_reader, ResponseReader)
        self._name = name
        self._context = context
        self._request_reader = request_reader
        self._response_reader = response_reader
        self._custom_fields = custom_fields or {}

    @property
    def custom_fields(self):
        """ Get the custom fields """
        return self._custom_fields

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
