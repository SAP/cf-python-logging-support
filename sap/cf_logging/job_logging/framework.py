""" Framework to be used by worker/job running applications """
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.job_logging.context import JobContext
from sap.cf_logging.core.request_reader import RequestReader
from sap.cf_logging.core.response_reader import ResponseReader

JOB_FRAMEWORK_NAME = 'job.framework'


class JobFramework(Framework):
    """ Simple framework using default request and response readers.
    Uses JobContext to keeping properties in memory  """

    def __init__(self, context=None):
        super(JobFramework, self).__init__(
            JOB_FRAMEWORK_NAME,
            context or JobContext(),
            RequestReader(),
            ResponseReader()
        )
