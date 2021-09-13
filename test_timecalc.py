from timecalc import timedelta_to_str, calculate_total_time, ParseError, TimeRangeError
from datetime import timedelta

import pytest


@pytest.mark.parametrize(
    "args_list,expected_timedelta",
    [
        (["08:00-09:00"], timedelta(hours=1)),
        (["8:00-9:00"], timedelta(hours=1)),
        (["8-9"], timedelta(hours=1)),
        (["8-9:00"], timedelta(hours=1)),
        (["8:00-9"], timedelta(hours=1)),
        (["08:00-09:00", "10:00-11:31"], timedelta(hours=2, minutes=31)),
    ],
)
def test_parsing_time_range(args_list, expected_timedelta):
    assert calculate_total_time(args_list) == expected_timedelta


@pytest.mark.parametrize(
    "args_list,expected_timedelta",
    [
        (["30m"], timedelta(minutes=30)),
        (["90m"], timedelta(hours=1, minutes=30)),
        (["1h", "90m"], timedelta(hours=2, minutes=30)),
        (["1h", "90m", "-30m"], timedelta(hours=2)),
        (["1d", "30m", "-1h"], timedelta(hours=23, minutes=30)),
        (["1w", "1d", "5h"], timedelta(weeks=1, days=1, hours=5)),
    ],
)
def test_parsing_time_intervals(args_list, expected_timedelta):
    assert calculate_total_time(args_list) == expected_timedelta


@pytest.mark.parametrize(
    "args_list,expected_timedelta",
    [
        (["30m", "12-15"], timedelta(hours=3, minutes=30)),
        (["12-15", "30m"], timedelta(hours=3, minutes=30)),
        (["12-15", "-30m"], timedelta(hours=2, minutes=30)),
    ],
)
def test_parsing_mixed_input(args_list, expected_timedelta):
    assert calculate_total_time(args_list) == expected_timedelta


@pytest.mark.parametrize(
    "args_list,expected_output",
    [
        (["8-9", "10:00-11:30"], "2h 30m"),
        (["8-9", "-15m"], "45m"),
        (["20:00-23:04", "-25m", "52m"], "3h 31m"),
        (["1h"], "1h"),
        (["1m"], "1m"),
        (["1d"], "1d"),
        (["1w"], "1w"),
        (["1d", "1m"], "1d 1m"),
        (["1w", "1d", "1m"], "1w 1d 1m"),
        (["1w", "1m"], "1w 1m"),
        (["1w", "1h"], "1w 1h"),
        (["1w", "1d", "1h", "1m"], "1w 1d 1h 1m"),
    ],
)
def test_total_time_formatting(args_list, expected_output):
    assert timedelta_to_str(calculate_total_time(args_list)) == expected_output


@pytest.mark.parametrize(
    "args_list,expected_output",
    [
        (["1h", "-1h"], "0h"),
        (["1d", "-24h"], "0h"),
    ],
)
def test_zero_result(args_list, expected_output):
    assert timedelta_to_str(calculate_total_time(args_list)) == expected_output


@pytest.mark.parametrize(
    "args_list,expected_exception",
    [
        ([""], ParseError),
        (["invalid"], ParseError),
        (["1x"], ParseError),
        (["7:00-"], ParseError),
        (["7-"], ParseError),
        (["7:-4"], ParseError),
        (["24:00-9:00"], ParseError),
        (["23:59-00:00"], TimeRangeError),
    ],
)
def test_parse_exception(args_list, expected_exception):
    with pytest.raises(expected_exception):
        calculate_total_time(args_list)
