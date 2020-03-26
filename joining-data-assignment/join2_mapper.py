#!/usr/bin/python

"""Mapper for data join.

Takes <TV show, viewer count> and <TV show, channel> pairs as input, 
outputs <TV show, viewer count> pairs and <TV show, channel> pairs 
if channel is "ABC".
"""

import sys


for line in sys.stdin:
    line = line.strip()   #strip out carriage return
    key, val = line.split(",")
    val = val.lstrip()

    if val == "ABC" or val.isdigit():
        print("{0},{1}".format(key, val))
