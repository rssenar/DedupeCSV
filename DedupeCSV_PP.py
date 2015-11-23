'''
8888888b.                888                             .d8888b.   .d8888b.  888     888         8888888b.  8888888b.  
888  "Y88b               888                            d88P  Y88b d88P  Y88b 888     888         888   Y88b 888   Y88b 
888    888               888                            888    888 Y88b.      888     888         888    888 888    888 
888    888  .d88b.   .d88888 888  888 88888b.   .d88b.  888         "Y888b.   Y88b   d88P         888   d88P 888   d88P 
888    888 d8P  Y8b d88" 888 888  888 888 "88b d8P  Y8b 888            "Y88b.  Y88b d88P          8888888P"  8888888P"  
888    888 88888888 888  888 888  888 888  888 88888888 888    888       "888   Y88o88P           888        888        
888  .d88P Y8b.     Y88b 888 Y88b 888 888 d88P Y8b.     Y88b  d88P Y88b  d88P    Y888P            888        888        
8888888P"   "Y8888   "Y88888  "Y88888 88888P"   "Y8888   "Y8888P"   "Y8888P"      Y8P    88888888 888        888        
                                      888                                                                               
                                      888                                                                               
                                      888                                                                               
'''
# ---------------------------------------------
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
