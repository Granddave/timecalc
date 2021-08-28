# Timecalc

Simple CLI tool that calculates the total time spent on a project given time ranges and time
intervals.

## How to use

```bash
$ ./timecalc.py --help
usage: timecalc.py [-h] time_parts [time_parts ...]

Calculates the total time of a given set of time ranges and intervals

positional arguments:
  time_parts  Time ranges or intervals, e.g. 09:00-12:30, 1h and 30m

optional arguments:
  -h, --help  show this help message and exit
```

Let's say that you work the whole morning and have a daily standup for 15 minutes and a coffe break
for 30 minutes:

```bash
$ ./timecalc.py 07:00-12:00 -15m -30m
Total time: 04:15
```

## Requirements

- Python >=3.8
- Docker for testing

## Run tests

```bash
$ ./run-tests.sh
```
