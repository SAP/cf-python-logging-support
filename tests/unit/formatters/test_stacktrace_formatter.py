import logging
import sys
from unittest.mock import patch

from sap.cf_logging.formatters.stacktrace_formatter import StacktraceFormatter


STACKTRACE = ''.join(['Traceback (most recent call last):\n',
'File "nonexistent_file.py", line 100, in nonexistent_function\n',
'raise ValueError("Oh no")\n',
'ValueError: Oh no'])


def test_stacktrace_not_truncated():
    fmt = StacktraceFormatter(STACKTRACE)
    formatted = fmt.format()
    assert "TRUNCATED" not in formatted
    assert "OMITTED" not in formatted


@patch('sap.cf_logging.core.constants.STACKTRACE_MAX_SIZE', 120)
def test_stacktrace_truncated():
    fmt = StacktraceFormatter(STACKTRACE)
    formatted = fmt.format()
    assert "TRUNCATED" in formatted
    assert "OMITTED" in formatted