from timecalc import timedelta_to_str, calculate_total_time, ParseError
from datetime import timedelta

import pytest


def test_input_calculations():
    assert calculate_total_time(["08:00-09:00"]) == timedelta(hours=1)
    assert calculate_total_time(["8:00-9:00"]) == timedelta(hours=1)
    assert calculate_total_time(["8-9"]) == timedelta(hours=1)
    assert calculate_total_time(["8-9:00"]) == timedelta(hours=1)
    assert calculate_total_time(["08:00-09:00", "10:00-11:30"]) == timedelta(hours=2, minutes=30)

    assert calculate_total_time(["30m"]) == timedelta(minutes=30)
    assert calculate_total_time(["90m"]) == timedelta(hours=1, minutes=30)
    assert calculate_total_time(["1h", "90m"]) == timedelta(hours=2, minutes=30)
    assert calculate_total_time(["1h", "90m", "-30m"]) == timedelta(hours=2)
    assert calculate_total_time(["2h", "-30m", "-1h"]) == timedelta(minutes=30)

    assert calculate_total_time(["08:00-09:00", "-15m"]) == timedelta(minutes=45)


def test_total_time_formatting():
    assert timedelta_to_str(calculate_total_time(["08:00-09:00", "10:00-11:30"])) == "02:30"
    assert timedelta_to_str(calculate_total_time(["08:00-09:00", "-15m"])) == "00:45"


def test_parse_exception():
    with pytest.raises(ParseError):
        calculate_total_time(["invalid"])
        calculate_total_time(["1d"])
        calculate_total_time(["7:00-"])
        calculate_total_time(["7-"])
        calculate_total_time(["7:-4"])
    with pytest.raises(ValueError):
        calculate_total_time(["23:59-00:00"])
