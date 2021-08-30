
[![Python package](https://github.com/Granddave/timecalc/actions/workflows/ci.yml/badge.svg)](https://github.com/Granddave/timecalc/actions/workflows/ci.yml)

# Timecalc 

Simple CLI tool that calculates the total time spent on a project given time ranges and intervals.

## How to use

```bash
$ ./timecalc.py --help
usage: timecalc.py [-h] time_parts [time_parts ...]

Calculates the total time of a given set of time ranges and intervals

positional arguments:
  time_parts  Time ranges or intervals, e.g. 9:00-12:30, 1h or -30m

optional arguments:
  -h, --help  show this help message and exit
```

Let's say that you work the whole morning and have a daily standup for 15 minutes and a coffe break
for 30 minutes. In the afternoon you work two hours:

```bash
$ ./timecalc.py 7:00-12:00 -15m -30m 2h
6h 15m
```

## Requirements

- Python >=3.6
