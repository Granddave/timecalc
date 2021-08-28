#!/bin/sh

docker build -t timecalc-test .
docker run -it --rm timecalc-test
