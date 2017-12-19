""" Util module with helper functions """
import json
import os

from sap.cf_logging.defaults import UNIX_EPOCH

VCAP_APPLICATION = json.loads(os.getenv('VCAP_APPLICATION', default='{}'))


def get_vcap_param(param_name, default=None):
    """
    Returns a parameter from the VCAP_APPLICATION environment variable
    :param param_name: the name of the parameter
    :param default: a default value if it cannot be found
    :return: The value of the parameter, the default if it cannot be found,
    or '-' if the default is not specified.
    """
    return VCAP_APPLICATION.get(param_name, default)


def epoch_nano_second(datetime_):
    """ Returns the nanoseconds since epoch time """
    return int((datetime_ - UNIX_EPOCH).total_seconds()) * 1000000000 + datetime_.microsecond * 1000


def iso_time_format(datetime_):
    """ Returns ISO time formatted string """
    return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (
        datetime_.year, datetime_.month, datetime_.day, datetime_.hour,
        datetime_.minute, datetime_.second, int(datetime_.microsecond / 1000))


def time_delta_ms(start, end):
    """ Returns the delta time between to datetime objects """
    time_delta = end - start
    return int(time_delta.total_seconds()) * 1000 + \
           int(time_delta.microseconds / 1000)


def parse_int(_int, default):
    """ Parses an int and returns the result
        A default can be provided in case the parse fails
    """
    try:
        integer = int(_int)
    except:  # pylint: disable-msg=bare-except
        integer = default
    return integer
