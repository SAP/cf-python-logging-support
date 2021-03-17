""" Module testing the functionality of the StacktraceFormatter class """
from sap.cf_logging.formatters.stacktrace_formatter import format_stacktrace


STACKTRACE = ''.join(['Traceback (most recent call last):\n',
                      'File "nonexistent_file.py", line 100, in nonexistent_function\n',
                      'raise ValueError("Oh no")\n',
                      'ValueError: Oh no'])


def test_stacktrace_not_truncated():
    """ Test that stacktrace is not truncated when smaller than the stacktrace maximum size """
    formatted = format_stacktrace(STACKTRACE)
    assert "TRUNCATED" not in formatted
    assert "OMITTED" not in formatted


def test_stacktrace_truncated(monkeypatch):
    """ Test that stacktrace is truncated when bigger than the stacktrace maximum size """
    monkeypatch.setattr('sap.cf_logging.core.constants.STACKTRACE_MAX_SIZE', 120)

    formatted = ''.join(format_stacktrace(STACKTRACE))
    assert "TRUNCATED" in formatted
    assert "OMITTED" in formatted
