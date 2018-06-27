""" Module for a stacktrace formatter """
import logging
import re

from sap.cf_logging.core import constants


class StacktraceFormatter:
    """
    Formats an exception stacktrace
    returned by a user logger.exception call
    Removes newline and tab characters
    Truncates stacktrace to maximum size
    """

    def __init__(self, stacktrace):
        self.stacktrace = stacktrace

    def format(self):
        stacktrace = re.sub('\n|\t', '  ', self.stacktrace)

        if len(stacktrace) <= constants.STACKTRACE_MAX_SIZE:
            return stacktrace

        stacktrace_beginning = StacktraceFormatter.stacktrace_beginning(
            stacktrace, constants.STACKTRACE_MAX_SIZE // 3
        )

        stacktrace_end = StacktraceFormatter.stacktrace_end(
            stacktrace, (constants.STACKTRACE_MAX_SIZE // 3) * 2
        )

        new_stacktrace = "-------- STACK TRACE TRUNCATED --------" + stacktrace_beginning +\
                         "-------- OMITTED --------" + stacktrace_end

        return new_stacktrace

    @staticmethod
    def stacktrace_length(stacktrace):
        return len(stacktrace)

    @staticmethod
    def stacktrace_beginning(stacktrace, size):
        if len(stacktrace) <= size:
            return stacktrace

        return stacktrace[:size]

    @staticmethod
    def stacktrace_end(stacktrace, size):
        l = StacktraceFormatter.stacktrace_length(stacktrace)
        if l <= size:
            return stacktrace

        return stacktrace[l-size:l]