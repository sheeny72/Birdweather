# Birdweather
Python code for Birdweather Reports

# Bird Report 5.py
Bird Report 5 takes a CSV files as exported from Birdweather Data Explorer and produces two Pivot table Reports.
The first pivot table displays the time of day of calls (grouped by hour) for each species.
The second pivot table displays the calls per day for each species.

It is recommended the CSV file exported from Birdweather is renamed with a suitable filename convention to easily identify file contents.
The convention I chose to use is 9999 LLLLLL MMM YY, where 9999 is the device number on Birdweather, LLLLLL is the location of the devise at the time of recording, MMM is the month, and YY is the year.

The code saves the final pivot tables as both CSV files (for further processing if required) and a PNG files (for display).

Required Input:
Station Name onlines 37 to 46. (Multiple lines allow for multiple stations and locations).
Location on lines 37 to 46.
Filename of the source CSV file on line 47

The date range of the report is read from the source CSV file.

Reports are sorted by Common Name of the species to make finding a species easier.

Example out files are: 4632 Butterfactory Lane June 24*.*
