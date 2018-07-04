import logging

from django.http import HttpResponse
from django.views import generic

from sap.cf_logging.core.constants import REQUEST_KEY
from tests.util import config_logger, check_log_record
from tests.log_schemas import JOB_LOG_SCHEMA


class IndexView(generic.View):
    def get(self, request):
        return HttpResponse("Hello test!", content_type='text/plain')


class UserLoggingView(generic.View):
    def get(self, request, *args, **kwargs):
        expected = kwargs.get('expected') or {}
        extra = kwargs.get('extra') or {}
        extra.update({REQUEST_KEY: request})

        self.logger, self.stream = config_logger('user.logging')
        self.logger.log(logging.INFO, 'in route headers', extra=extra)
        assert check_log_record(self.stream, JOB_LOG_SCHEMA, expected) == {}
        return HttpResponse("ok", content_type='text/plain')
