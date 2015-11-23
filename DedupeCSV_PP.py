#!/usr/bin/python3.4.3
# ---------------------------------------------
# Imports
# ---------------------------------------------
import csv
# ---------------------------------------------
# Global Variables
# ---------------------------------------------
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
InputFile = "DedupeSampleData.csv" 
CleanOutput = "_CleanOutputPP.csv"
Dupes = "_DupesPP.csv" 
# ---------------------------------------------w
FName = 0
LName = 1
Address = 2
Zip = 5
Entries = set()
# ----------------------------------------------
# Objects
# ----------------------------------------------
Input = csv.reader(open(InputFile,'r'))
OutputClean = csv.writer(open(CleanOutput,'a'))
OutDupes = csv.writer(open(Dupes,'a'))
OutputClean.writerow(['FName','LName','Address','City','State','Zip','VIN','Year','Make','Model'])
OutDupes.writerow(['FName','LName','Address','City','State','Zip','VIN','Year','Make','Model'])
# ----------------------------------------------
# Main Program
# ----------------------------------------------
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		key = (line[FName],line[LName],line[Address],line[Zip])
		if key not in Entries:
			OutputClean.writerow(line)
			Entries.add(key)
		else:
			OutDupes.writerow(line)
