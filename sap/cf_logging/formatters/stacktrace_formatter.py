""" Module for a stacktrace formatter """
import re

from sap.cf_logging.core import constants


class StacktraceFormatter:
    """
    Formats an exception stacktrace
    returned by a user logger.exception call
    """

    def __init__(self, stacktrace):
        self.stacktrace = stacktrace

    def format(self):
        """
        Removes newline and tab characters
        Truncates stacktrace to maximum size
        """
        stacktrace = re.sub('\n|\t', '  ', self.stacktrace)

        if len(stacktrace) <= constants.STACKTRACE_MAX_SIZE:
            return stacktrace

        stacktrace_beginning = self.stacktrace_beginning(
            constants.STACKTRACE_MAX_SIZE // 3
        )

        stacktrace_end = self.stacktrace_end(
            (constants.STACKTRACE_MAX_SIZE // 3) * 2
        )

        new_stacktrace = "-------- STACK TRACE TRUNCATED --------" + stacktrace_beginning +\
                         "-------- OMITTED --------" + stacktrace_end

        return new_stacktrace

    @property
    def stacktrace_length(self):
        """ Gets the length of the stacktrace """
        return len(self.stacktrace)

    def stacktrace_beginning(self, size):
        """ Gets the first `size` bytes of the stacktrace """
        if self.stacktrace_length <= size:
            return self.stacktrace

        return self.stacktrace[:size]

    def stacktrace_end(self, size):
        """ Gets the last `size` bytes of the stacktrace """
        if self.stacktrace_length <= size:
            return self.stacktrace

        return self.stacktrace[:-(self.stacktrace_length-size)]
