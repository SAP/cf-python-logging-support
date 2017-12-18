""" Tests `record.util` package """
from datetime import datetime

from sap.cf_logging.defaults import UNIX_EPOCH
from sap.cf_logging.record import util


def test_parse_int_default():
    """ test util.parse_int will return default for invalid input"""
    assert util.parse_int('1a23', 3) == 3
    assert util.parse_int('{}', -1) == -1


def test_parse_int():
    """ test util.parse_int works correctly """
    assert util.parse_int('194', 5) == 194
    assert util.parse_int(9811, -1) == 9811


def test_epoch_nano_second():
    """ test util.epoch_nano_second calculates correctly """
    date = datetime(2017, 1, 1, 0, 0, 0, 12)
    nanoseconds = 1483228800000012000
    assert util.epoch_nano_second(date) == nanoseconds


def test_iso_time_format():
    """ test util.iso_time_format builds ISO date string """
    date = datetime(2017, 1, 5, 1, 2, 3, 2000)
    assert util.iso_time_format(date) == '2017-01-05T01:02:03.002Z'


def test_time_delta_ms():
    """ test time_delta_ms calculates delta between date and unix epoch"""
    date = datetime(2017, 1, 1, 0, 0, 0, 12000)
    assert util.time_delta_ms(UNIX_EPOCH, date) == 1483228800012
