""" Module that contains the CfLogger class """
import logging
import sys

from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.formatters.json_formatter import JsonFormatter
from sap.cf_logging.job_logging.framework import JobFramework
from sap.cf_logging.record.request_log_record import RequestWebRecord
from sap.cf_logging.record.simple_log_record import SimpleLogRecord

__version__ = '4.0.1'

_SETUP_DONE = False
FRAMEWORK = None


class CfLogger(logging.Logger):
    """ CfLogger class inherits from logging.Logger and makes custom
        log messages
    """

    # pylint: disable=too-many-arguments,arguments-differ,keyword-arg-before-vararg
    def makeRecord(self, name, level, fn, lno, msg, msgargs, exc_info,
                   func=None, extra=None, *args, **kwargs):
        """ Returns SimpleLogMessage or a RequestWebRecord depending on the extra variable """
        # check what record type this is
        cls = None
        if extra is not None and REQUEST_KEY in extra and RESPONSE_KEY in extra:
            cls = RequestWebRecord
        else:
            cls = SimpleLogRecord

        return cls(extra, FRAMEWORK, name, level, fn, lno, msg, msgargs, exc_info,
                   func, *args, **kwargs)

def init(cfl_framework=None, level=defaults.DEFAULT_LOGGING_LEVEL):
    """ Initialize function. It sets up the logging library to output JSON
        formatted messages.

        Optional arguments framework to use and logging.level
    """
    global FRAMEWORK  # pylint: disable=global-statement
    global _SETUP_DONE  # pylint: disable=global-statement
    if _SETUP_DONE:
        raise RuntimeError('cf_logging already initialized')

    if cfl_framework is not None and not isinstance(cfl_framework, Framework):
        raise TypeError('expecting framework of type {}'.format(Framework.__name__))

    _SETUP_DONE = True
    FRAMEWORK = cfl_framework or JobFramework()

    logging.setLoggerClass(CfLogger)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
