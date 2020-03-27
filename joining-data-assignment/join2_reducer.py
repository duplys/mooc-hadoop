#!/usr/bin/python

import sys

"""Reducer for joining data.

Takes pairs <TV show, viewer count> and <TV show, channel> where channel is "ABC".
Outputs pairs <TV show<space>total viewer count> with the total viewer count
(across all channels) for shows that are aired on "ABC" (and, potentially, also 
on other channels).

Due to MapReduce shuffle & sort, the input pairs are sorted in this order:

...
Almost_Cooking,980
Almost_Cooking,998
Almost_Games,1006
...
Almost_Games,996
Almost_Games,ABC
Almost_News,1003
Almost_News,101
...

So if we keep the running total viewer count for a TV show, the key 
(i.e., the TV show name) changes, and the last pair had "ABC" as its value,
then we can print the pair <TV show, total viewer count> to answer the 
question: "what is the total number of viewers for shows on ABC?".

Remark: I personally find the above question ambiguous, because it could also
mean that you need to find the total number of ABC viewers for shows that
run on ABC. Instead, the question should be "what is the total number of
viewers for shows aired on ABC? (including the vierwers of these shows
on different channels)".
"""

prev_word          = "  "                #initialize previous word  to blank string
months             = ['Jan','Feb','Mar','Apr','Jun','Jul','Aug','Sep','Nov','Dec']

dates_to_output    = [] #an empty list to hold dates for a given word
day_cnts_to_output = [] #an empty list of day counts for a given word
# see https://docs.python.org/2/tutorial/datastructures.html for list details

line_cnt           = 0  #count input lines

previous_tv_show = ""
previous_val = ""
total_viewer_count = 0

for line in sys.stdin:
    tv_show, val = line.strip().split(",")   # strip carriage return and split at comma

    # if we see a new TV show, reset the total_viewer_count to 0
    if tv_show != previous_tv_show:
        if previous_val == "ABC":
            print("{0} {1}".format(previous_tv_show, total_viewer_count))

        total_viewer_count = 0

    # if the value is a digit, add it to the total viewer count
    if val.isdigit():
        total_viewer_count += int(val)

    previous_tv_show = tv_show
    previous_val = val