#!/usr/bin/python

import sys

"""Mapper for joining data.

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
total_viewer_count = 0

for line in sys.stdin:
    key, val = line.strip().split(",")   # strip carriage return and split at comma

    if val.isdigit():
        total_viewer_count += int(val)


    tv_show = key    

    if tv_show != previous_tv_show:
    

    previous_tv_show

    #note: for simple debugging use print statements, ie:  
    curr_word  = key_value[0]         #key is first item in list, indexed by 0
    value_in   = key_value[1]         #value is 2nd item

    #-----------------------------------------------------
    # Check if its a new word and not the first line 
    #   (b/c for the first line the previous word is not applicable)
    #   if so then print out list of dates and counts
    #----------------------------------------------------
    if curr_word != prev_word:

        # -----------------------     
	#now write out the join result, but not for the first line input
        # -----------------------
        if line_cnt>1:
	    for i in range(len(dates_to_output)):  #loop thru dates, indexes start at 0
	         print('{0} {1} {2} {3}'.format(dates_to_output[i],prev_word,day_cnts_to_output[i],curr_word_total_cnt))
            #now reset lists
	    dates_to_output   =[]
            day_cnts_to_output=[]
        prev_word         =curr_word  #set up previous word for the next set of input lines

	
    # ---------------------------------------------------------------
    #whether or not the join result was written out, 
    #   now process the curr word    
  	
    #determine if its from file <word, total-count> or < word, date day-count>
    # and build up list of dates, day counts, and the 1 total count
    # ---------------------------------------------------------------
    if (value_in[0:3] in months): 

        date_day =value_in.split() #split the value field into a date and day-cnt
        
        #add date to lists of the value fields we are building
        dates_to_output.append(date_day[0])
        day_cnts_to_output.append(date_day[1])
    else:
        curr_word_total_cnt = value_in  #if the value field was just the total count then its
                                           #the first (and only) item in this list

# ---------------------------------------------------------------
#now write out the LAST join result
# ---------------------------------------------------------------
for i in range(len(dates_to_output)):  #loop thru dates, indexes start at 0
         print('{0} {1} {2} {3}'.format(dates_to_output[i],prev_word,day_cnts_to_output[i],curr_word_total_cnt))