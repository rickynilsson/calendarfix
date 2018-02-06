# calendarfix
Fixes Google Calendar with "No Title" events 

This script removes events with empty SUMMARY keyword from your calendar (ics) file. Event entries with empty SUMMARY will show up as events named "(No Title)" in your Google Calendar, which can happen if something goes wrong when importing events from other calendars. If you have many of these entries and don't feel like deleting them one-by-one, just export your ics file and remove them with this script. Please note that deleting any events/meetings with invited guests in Google Calendar will send a message to those guests that you've declined or cancelled the event. Use at own risk!  Tested in Python 3.4.5
