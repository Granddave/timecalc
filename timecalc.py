#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import re
import sys
from typing import Optional, List


_time_range_re = re.compile(
    r"^((?:(?:[0-1]?\d)|(?:2[0-3]))(?::[0-5]\d)?)-((?:(?:[0-1]?\d)|(?:2[0-3]))(?::[0-5]\d)?)$"
)
_time_interval_re = re.compile(r"^(-?\d+[wdmh])$")


class ParseError(Exception):
    pass


class NegativeTimeDelta(Exception):
    pass


def _match_time_range(timerange_str: str) -> Optional[List[str]]:
    match = _time_range_re.findall(timerange_str)
    if match:
        return match[0]
    return None


def _match_time_interval(timeinterval_str: str) -> Optional[str]:
    match = _time_interval_re.findall(timeinterval_str)
    if match:
        return match[0]
    return None


def _convert_time_str(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%H:%M" if ":" in time_str else "%H")


def _calculate_time_range(start_str: str, end_str: str) -> timedelta:
    start_time = _convert_time_str(start_str)
    end_time = _convert_time_str(end_str)

    if end_time < start_time:
        raise ValueError(f"End time cannot be before start time: '{start_str}-{end_str}'")

    return end_time - start_time


def _calculate_time_interval(interval: str) -> timedelta:
    """Convert time interval string to timedelta object"""
    time_range_units = {
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks",
    }
    return timedelta(**{time_range_units[interval[-1]]: int(interval[:-1])})


def calculate_total_time(args_list: List[str]) -> timedelta:
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

        raise ParseError(f"Failed to parse '{item}'")
    return total_time


def timedelta_to_str(delta: timedelta) -> str:
    """Constructs a Jira work log formatted string from a timedelta object"""
    weeks = delta.days // 7
    days = delta.days % 7
    hours = delta.seconds // 3600
    minutes = delta.seconds // 60 % 60

    output = f"{weeks}w " if weeks != 0 else ""
    output += f"{days}d " if days != 0 else ""
    output += f"{hours}h " if hours > 0 else ""
    output += f"{minutes}m " if minutes > 0 else ""
    return output.strip()


def _print_help():
    print(
        f"""usage: {sys.argv[0]} [-h] time_parts [time_parts ...]

Calculates the total time of a given set of time ranges and intervals

positional arguments:
  time_parts  Time ranges or intervals, e.g. 09:00-12:30, 1h or -30m

optional arguments:
  -h, --help  show this help message and exit"""
    )


def _main():
    args = sys.argv
    if len(args) == 1:
        _print_help()
        sys.exit(1)

    if any(x in ["-h", "--help"] for x in args):
        _print_help()
        sys.exit(0)

    parts = args[1:]

    try:
        total_time = calculate_total_time(parts)
        print(timedelta_to_str(total_time))
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    _main()
