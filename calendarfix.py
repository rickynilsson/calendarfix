#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This script removes events with empty SUMMARY keyword from your calendar (ics) file. Event entries with empty SUMMARY will show up as events named "(No Title)" in your Google Calendar, which can happen if something goes wrong when importing events from other calendars. If you have many of these entries and don't feel like deleting them one-by-one, just export your ics file and remove them with this script. Please note that deleting any events/meetings with invited guests in Google Calendar will send a message to those guests that you've declined or cancelled the event. Use at own risk!

Tested in Python 3.4.5
'''

lines = [] # Empty list for lines in ics file

with open('yourcalendar.ics', 'rt') as in_file:  # Open your calendar ics file for reading of data
    for line in in_file: # For each line in file
        lines.append(line)  # Add that line to list of lines

header = [] # Empty list for calendar header lines (before first event)
for m in lines[0:43]:
    header.append(m) # Add header lines to header list

footer = [lines[-1]] # Create footer list from footer line (last line after events)

eventstartlines = [] # Empty list for event start line numbers
eventendlines = [] # Empty list for event end line numbers
eventsummarylines = [] # Empty list for event summary line numbers
for lineno in range(len(lines)): # For each line in list, check for event start/end/summary. If there, append line number to respective lists.
    if lines[lineno].find('BEGIN:VEVENT\n') != -1:
        eventstartlines.append(lineno)
    if lines[lineno].find('END:VEVENT\n') != -1:
        eventendlines.append(lineno)
    if lines[lineno].find('SUMMARY:') != -1:
        eventsummarylines.append(lineno)

nevents = len(eventstartlines) # Number of events

eventstartlines_afterclean = [] # Empty list for event start line numbers after cleaning out events with empty SUMMMARY
eventendlines_afterclean = [] # Empty list for event end line numbers after cleaning out events with empty SUMMARY
for eventno in range(nevents): # For each event
    if lines[eventsummarylines[eventno]].find('SUMMARY:\n') == -1: # Check if SUMMARY not empty
        eventstartlines_afterclean.append(eventstartlines[eventno]) # Add to new start line list
        eventendlines_afterclean.append(eventendlines[eventno]) # Add to new end line list

nevents_afterclean = len(eventstartlines_afterclean) # Number of events remaining after removing the ones with empty SUMMARY


### Gather all events with non-empty SUMMARY. You can do the below in one loop, but if your ics file is larger than 1 MB Google won't import it, and you'll have to split into several ics files (4 below)

eventlines_afterclean_1 = []
for eventno in range(0,int(nevents_afterclean/4)):
    for lineno in range(eventstartlines_afterclean[eventno],eventendlines_afterclean[eventno]+1):
        eventlines_afterclean_1.append(lines[lineno])

eventlines_afterclean_2 = []
for eventno in range(int(nevents_afterclean/4),2*int(nevents_afterclean/4)):
    for lineno in range(eventstartlines_afterclean[eventno],eventendlines_afterclean[eventno]+1):
        eventlines_afterclean_2.append(lines[lineno])

eventlines_afterclean_3 = []
for eventno in range(2*int(nevents_afterclean/4),3*int(nevents_afterclean/4)):
    for lineno in range(eventstartlines_afterclean[eventno],eventendlines_afterclean[eventno]+1):
        eventlines_afterclean_3.append(lines[lineno])

eventlines_afterclean_4 = []
for eventno in range(3*int(nevents_afterclean/4),4*int(nevents_afterclean/4)):
    for lineno in range(eventstartlines_afterclean[eventno],eventendlines_afterclean[eventno]+1):
        eventlines_afterclean_4.append(lines[lineno])

# Assemble lines to complete lists with headers, events, and footers
newlines1 = header + eventlines_afterclean_1 + footer 
newlines2 = header + eventlines_afterclean_2 + footer 
newlines3 = header + eventlines_afterclean_3 + footer
newlines4 = header + eventlines_afterclean_4 + footer  

# Write the calendar ics files
fh = open('cleaned_cal_part1.ics','w') 
fh.writelines(newlines1) 
fh.close()

fh = open('cleaned_cal_part2.ics','w') 
fh.writelines(newlines2) 
fh.close()

fh = open('cleaned_cal_part3.ics','w') 
fh.writelines(newlines3) 
fh.close()

fh = open('cleaned_cal_part4.ics','w') 
fh.writelines(newlines4) 
fh.close()

# When done, import your cleaned ics files into Google Calendar.