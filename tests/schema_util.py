""" Common utils and defaults used in the tests"""

WORD = r'.+'
TEXT = r'.*'
STRING_NUM = r'[\d+|-]'
IP = r'[[0-9]+|.?]+\d$'
HOST_NAME = r'[[0-9]+|.?]+\d$'

LEVEL = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']


def num(val=None):
    """ Return validation schema for numbers """
    if val is None:
        return {'type': int}
    return {
        'type': int,
        'gt': val - 1,
        'lt': val + 1
    }


def pos_num():
    """ Return validation schema for positive numbers """
    return {
        'type': int,
        'gt': -1,
        'gt_error': 'Not a positive number'
    }


def string(regex):
    """ Return validation schema for strings """
    return {
        'format': regex,
        'format_error': 'Incorrect {value} string value'
    }


def enum(lst):
    """ Return validation schema for lists """
    return {
        'in': lst,
        'in_error': 'Value not in list of expected values'
    }


def iso_datetime():
    """ Return validation schema for datetime """
    return {
        'format': r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z',
        'format_error': 'Invalid date format'
    }


def extend(dict1, dict2):
    """ Extend dict1 with dict2 """
    new_dict = dict1.copy()
    new_dict.update(dict2)
    return new_dict
