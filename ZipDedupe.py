#!/usr/bin/python3.4.3
# Required Modules
import csv
# ---------------------------------------------
# GLOBAL VARIABLE
# ---------------------------------------------
InputFile = "/Users/rssenar/Desktop/free-zipcode-database MASTER.csv" 
# ---------------------------------------------
OutputFile = "/Users/rssenar/Desktop/_CLEANED US ZIP CODE COORDINATES.csv"
Dupes = "/Users/rssenar/Desktop/_Dupes.csv" 
# ---------------------------------------------
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
Zip = 0
latitude = 1
Longitude = 2
# ---------------------------------------------
HeaderRow = [\
	'Zip',\
	'Latitude',\
	'Longitude',\
	]
# ---------------------------------------------
# OBJECTS
# ---------------------------------------------
Input = csv.reader(open(InputFile,'r')) # Read in the input file
Output = csv.writer(open(OutputFile,'a')) # Open Clean output file
OutDupes = csv.writer(open(Dupes,'a')) # Open Dupes file
Output.writerow(HeaderRow) # Append Header Row to Clean output file
OutDupes.writerow(HeaderRow) # Append Header Row to Dupes file
# ---------------------------------------------
Entries = set()
# ---------------------------------------------
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		key = line[Zip]
		if key not in Entries: # Check if key is in the Entries set
			Output.writerow(line) # write to processed output file
			Entries.add(key) # add row to Entries set
		else:
			OutDupes.writerow(line) # write to Dupes file
