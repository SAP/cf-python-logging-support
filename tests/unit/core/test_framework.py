""" Tests `core.framework` """
import pytest
from sap.cf_logging.core.context import Context
from sap.cf_logging.core.request_reader import RequestReader
from sap.cf_logging.core.response_reader import ResponseReader
from sap.cf_logging.core.framework import Framework

# pylint: disable=abstract-method,  abstract-method, missing-docstring, invalid-name

context = Context()
request_reader = RequestReader()
response_reader = ResponseReader()


@pytest.mark.parametrize('initializers', [
    {'context': None, 'request_reader': request_reader, 'response_reader': response_reader},
    {'context': {}, 'request_reader': request_reader, 'response_reader': response_reader},
    {'context': context, 'request_reader': None, 'response_reader': response_reader},
    {'context': context, 'request_reader': {}, 'response_reader': response_reader},
    {'context': context, 'request_reader': request_reader, 'response_reader': None},
    {'context': context, 'request_reader': request_reader, 'response_reader': {}}
])
@pytest.mark.xfail(raises=TypeError, strict=True)
def test_init(initializers):
    Framework('django', **initializers)


def test_init_accept_inherited():
    """ test Framework::init accepts inherited classes arguments """

    class MyContext(Context):
        pass

    class MyRequestReader(RequestReader):
        pass

    class MyResponseReader(ResponseReader):
        pass

    Framework('name', MyContext(), MyRequestReader(), MyResponseReader())


@pytest.mark.parametrize('name', [None, 123, ''])
@pytest.mark.xfail(raises=TypeError, strict=True)
def test_init_name(name):
    Framework(name, context, request_reader, response_reader)
