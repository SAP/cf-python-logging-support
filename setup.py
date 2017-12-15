''' setup.py '''
import ast
import re

from setuptools import find_packages
from setuptools import setup

_VERSION_REGEX = re.compile(r'__version__\s+=\s+(.*)')
with open('./sap/cf_logging/__init__.py', 'rb') as f:
    VERSION = str(ast.literal_eval(_VERSION_REGEX.search(f.read().decode('utf-8')).group(1)))

setup(
    name='sap_cf_logging',
    version=VERSION,
    url='https://github.com/SAP/cf-python-logging-support',
    license='Apache License, Version 2.0',
    author='SAP',
    description='Python logging library to emit JSON logs in a SAP CloudFoundry environment',
    long_description_content_type='text/x-rst',
    packages=find_packages(include=['sap*']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[  # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development',
        'Topic :: System :: Logging',
    ]
)
