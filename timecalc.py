#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import re


_time_range_re = re.compile(r"^(\d{1,2}:\d{2})-(\d{1,2}:\d{2})$")
_time_interval_re = re.compile(r"^(-?\d{1,2}[mh])$")


class ParseError(RuntimeError):
    pass


def _match_time_range(timerange_str: str):
    match = _time_range_re.findall(timerange_str)
    if match:
        return match[0]
    return None


def _match_time_interval(timeinterval_str: str):
    match = _time_interval_re.findall(timeinterval_str)
    if match:
        return match[0]
    return None


def _calculate_time_range(t1: str, t2: str):
    format_string = "%H:%M"
    return datetime.strptime(t2, format_string) - datetime.strptime(t1, format_string)


def _calculate_time_interval(interval: str):
    """Convert time interval string to timedelta object"""
    time_range_units = {
        "m": "minutes",
        "h": "hours",
    }
    return timedelta(**{time_range_units[interval[-1]]: int(interval[:-1])})


def calculate_total_time(args_list):
    total_time = timedelta()
    for item in args_list:
        time_range = _match_time_range(item)
        if time_range:
            total_time += _calculate_time_range(time_range[0], time_range[1])
            continue

        time_interval = _match_time_interval(item)
        if time_interval:
            total_time += _calculate_time_interval(time_interval)
            continue

        raise ParseError(item)
    return total_time


def timedelta_to_str(delta: timedelta):
    """Creates a string with '%H:%M' format from a time delta"""
    parts = [int(x) for x in str(delta).split(":")]
    return f"{parts[0]:02d}:{parts[1]}"


def _main():
    parser = argparse.ArgumentParser(
        description="Calculates the total time of a given set of time ranges and intervals"
    )
    parser.add_argument(
        "time_parts",
        nargs="+",
        help="Time ranges or intervals, e.g. 09:00-12:30, 1h or -30m",
    )

    # Need to parse the parts like this to be able to support subtracting intervals, e.g. -15m
    args, unknown = parser.parse_known_args()
    parts = args.time_parts + unknown

    try:
        total_time = calculate_total_time(parts)
        print("Total time:", timedelta_to_str(total_time))
    except ParseError as e:
        print(f"Failed to parse '{e}'")


if __name__ == "__main__":
    _main()
