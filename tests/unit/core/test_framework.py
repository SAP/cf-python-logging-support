""" Tests `core.framework` """
import pytest
from sap.cf_logging.core.context import Context
from sap.cf_logging.core.request_reader import RequestReader
from sap.cf_logging.core.response_reader import ResponseReader
from sap.cf_logging.core.framework import Framework

# pylint: disable=abstract-method

CONTEXT = Context()
REQUEST_READER = RequestReader()
RESPONSE_READER = ResponseReader()


@pytest.mark.parametrize('initializers', [
    {'context': None, 'request_reader': REQUEST_READER, 'response_reader': RESPONSE_READER},
    {'context': {}, 'request_reader': REQUEST_READER, 'response_reader': RESPONSE_READER},
    {'context': CONTEXT, 'request_reader': None, 'response_reader': RESPONSE_READER},
    {'context': CONTEXT, 'request_reader': {}, 'response_reader': RESPONSE_READER},
    {'context': CONTEXT, 'request_reader': REQUEST_READER, 'response_reader': None},
    {'context': CONTEXT, 'request_reader': REQUEST_READER, 'response_reader': {}}
])
@pytest.mark.xfail(raises=TypeError, strict=True)
def test_init(initializers):
    """ test constructor with invalid context, request_reader and response_reader """
    Framework('django', **initializers)


def test_init_accept_inherited():
    """ test Framework::init accepts inherited classes arguments """

    class MyContext(Context): # pylint: disable=missing-docstring
        pass

    class MyRequestReader(RequestReader): # pylint: disable=missing-docstring
        pass

    class MyResponseReader(ResponseReader): # pylint: disable=missing-docstring
        pass

    Framework('name', MyContext(), MyRequestReader(), MyResponseReader())


@pytest.mark.parametrize('name', [None, 123, ''])
@pytest.mark.xfail(raises=TypeError, strict=True)
def test_init_name(name):
    """ test invalid 'name' provided to constructor """
    Framework(name, CONTEXT, REQUEST_READER, RESPONSE_READER)
