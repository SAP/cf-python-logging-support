import sys
import os

if sys.version_info < (3, 5):
    collect_ignore = ['tests/test_sanic_logging.py']

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.django_logging.example.settings'
