'''                                                                                                                           
 +-+-+-+-+-+-+ +-+-+-+
 |D|e|d|u|p|e| |C|S|V|
 +-+-+-+-+-+-+ +-+-+-+  
'''
#!/usr/bin/python3.4.3
# Required Modules
import csv
# ---------------------------------------------
'''
 +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+
 |G|l|o|b|a|l| |V|a|r|i|a|b|l|e|s|
 +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+
'''
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
InputFile = "MergeFile.csv" 
CleanOutput = "/Users/rssenar/Desktop/_CleanOutputPP.csv"
Dupes = "/Users/rssenar/Desktop/_DupesPP.csv" 
# ---------------------------------------------
# Select Criteria : 
# OPHH = One Record Per House Hold
# OPP = One Record Per Person
# VIN = Vin#
Selection = 'OPHH'
'''
+-+-+-+-+-+-+
|L|e|g|e|n|d|
+-+-+-+-+-+-+
'''
# Column[0] = CustomerID
# Column[1] = FirstName
# Column[2] = MI
# Column[3] = LastName
# Column[4] = Address
# Column[5] = City
# Column[6] = State
# Column[7] = Zip
# Column[8] = SCF
# Column[9] = Phone
# Column[10] = Email
# Column[11] = VIN
# Column[12] = TradeYear
# Column[13] = TradeMake
# Column[14] = TradeModel
# Column[15] = DelDate
# Column[16] = Date
# Column[17] = Radius
# Column[18] = Dupe1
# Column[19] = Dupe2
# Column[20] = Dupe3
# ---------------------------------------------
FName = 1 # First Name Field
LName = 3 # last Name Field
Address = 4 # Address Field
Zip = 7 # Zip Code Field
VIN = 11 # VIN Number Field
Entries = set() # Set Entries set to emplty
# ----------------------------------------------
''' 
 +-+-+-+-+-+-+-+
 |O|b|j|e|c|t|s|
 +-+-+-+-+-+-+-+ 
'''
# ----------------------------------------------
Input = csv.reader(open(InputFile,'r')) # Read in the input file
OutputClean = csv.writer(open(CleanOutput,'a')) # Open Processed output file
OutDupes = csv.writer(open(Dupes,'a')) # Open Dupes file
# Append Header Row to Processed output file
OutputClean.writerow(['CustomerID','FirstName','MI','LastName','Address','City','State','Zip','SCF',\
	'Phone','Email','VIN','TradeYear','TradeMake','TradeModel','DelDate','Date','Radius','Dupe1','Dupe2','Dupe3'])
# Append Header Row to Dupes file
OutDupes.writerow(['CustomerID','FirstName','MI','LastName','Address','City','State','Zip','SCF',\
	'Phone','Email','VIN','TradeYear','TradeMake','TradeModel','DelDate','Date','Radius','Dupe1','Dupe2','Dupe3'])
# ----------------------------------------------
'''
 +-+-+-+-+ +-+-+-+-+
 |M|a|i|n| |P|r|o|g|
 +-+-+-+-+ +-+-+-+-+
'''
# ----------------------------------------------
# Run test if CSV file has a header row
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		if Selection == 'OPHH': # Checks Selection Criteria
			key = (line[Address],line[Zip])
			if key not in Entries:
				OutputClean.writerow(line) # write to processed output file
				Entries.add(key) # add row to Entries set
			else:
				OutDupes.writerow(line) # write to Dupes file
		elif Selection == 'OPP': # Checks Selection Criteria
			key = (line[FName],line[LName],line[Address],line[Zip])
			if key not in Entries:
				OutputClean.writerow(line) # write to processed output file
				Entries.add(key) # add row to Entries set
			else:
				OutDupes.writerow(line) # write to Dupes file
		else:
			key = (line[VIN])
			if key not in Entries:
				OutputClean.writerow(line) # write to processed output file
				Entries.add(key) # add row to Entries set
			else:
				OutDupes.writerow(line) # write to Dupes file

