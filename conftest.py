import sys


if sys.version_info < (3, 5):
    collect_ignore = ['tests/test_sanic_logging.py']
