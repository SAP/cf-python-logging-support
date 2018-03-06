""" Module that contains the CfLogger class """
import logging
import sys

from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.record.request_log_record import RequestWebRecord
from sap.cf_logging.record.simple_log_record import SimpleLogRecord
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.formatters.json_formatter import JsonFormatter

__version__ = '3.1.1'

_setup_done = False  # pylint: disable=invalid-name
framework = None  # pylint: disable=invalid-name


class CfLogger(logging.Logger):
    """ CfLogger class inherits from logging.Logger and makes custom
        log messages
    """

    # pylint: disable=too-many-arguments,arguments-differ
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, *_args, **_kwargs):
        """ Returns SimpleLogMessage or a RequestWebRecord depending on the extra variable """
        # check what record type this is
        cls = None
        if extra is not None and REQUEST_KEY in extra and RESPONSE_KEY in extra:
            cls = RequestWebRecord
        else:
            cls = SimpleLogRecord

        return cls(extra, framework, name, level, fn, lno, msg, args, exc_info,
                   func, *_args, **_kwargs)


def init(cfl_framework=None, level=defaults.DEFAULT_LOGGING_LEVEL):
    """ Initialize function. It sets up the logging library to output JSON
        formatted messages.

        Optional arguments framework to use and logging.level
    """
    global framework  # pylint: disable=global-statement,invalid-name
    global _setup_done  # pylint: disable=global-statement,invalid-name
    if _setup_done:
        raise RuntimeError('cf_logging already initialized')

    if cfl_framework is not None and not isinstance(cfl_framework, Framework):
        raise TypeError('expecting framework of type {}'.format(Framework.__name__))

    _setup_done = True
    framework = cfl_framework

    logging.setLoggerClass(CfLogger)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
