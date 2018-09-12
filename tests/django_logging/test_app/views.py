""" Views for example django test app """
import logging

from django.http import HttpResponse
from django.views import generic

from sap.cf_logging.core.constants import REQUEST_KEY
from tests.util import config_logger, check_log_record
from tests.log_schemas import JOB_LOG_SCHEMA

# pylint: disable=unused-argument

class IndexView(generic.View):
    """ View that is hit on the index route """
    def get(self, request): # pylint: disable=no-self-use
        """ Return a basic http response """
        return HttpResponse("Hello test!", content_type='text/plain')


class UserLoggingView(generic.View):
    """ View that logs custom user information """
    provide_request = False

    def __init__(self, *args, **kwargs):
        self.logger, self.stream = config_logger('user.logging')
        super(UserLoggingView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """ Log a custom user message with the logger """
        expected = kwargs.get('expected') or {}
        extra = kwargs.get('extra') or {}
        if self.provide_request:
            extra.update({REQUEST_KEY: request})

        self.logger.log(logging.INFO, 'in route headers', extra=extra)
        assert check_log_record(self.stream, JOB_LOG_SCHEMA, expected) == {}
        return HttpResponse("ok", content_type='text/plain')
