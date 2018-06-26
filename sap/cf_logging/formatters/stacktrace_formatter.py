""" Module for a stacktrace formatter """
import logging
import re


class StacktraceFormatter(logging.Formatter):
    """
    Formats an exception stacktrace
    returned by a user logger.exception call
    Removes newline and tab characters
    Trims stacktrace to maximum size
    """

    def __init__(self, exc_info):
        self.exc_info = exc_info

    def formatException(self, exc_info):
        stacktrace = super(StacktraceFormatter, self).formatException(exc_info)

        stacktrace = re.sub('\n|\t', '  ', stacktrace)

        # TODO implement truncating stacktrace logic

        return stacktrace