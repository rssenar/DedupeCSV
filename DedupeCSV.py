'''
oooooooooo.                   .o8                                     .oooooo.    .oooooo..o oooooo     oooo
`888'   `Y8b                 "888                                    d8P'  `Y8b  d8P'    `Y8  `888.     .8'
 888      888  .ooooo.   .oooo888  oooo  oooo  oo.ooooo.   .ooooo.  888          Y88bo.        `888.   .8'
 888      888 d88' `88b d88' `888  `888  `888   888' `88b d88' `88b 888           `"Y8888o.     `888. .8'
 888      888 888ooo888 888   888   888   888   888   888 888ooo888 888               `"Y88b     `888.8'
 888     d88' 888    .o 888   888   888   888   888   888 888    .o `88b    ooo  oo     .d8P      `888'
o888bood8P'   `Y8bod8P' `Y8bod88P"  `V88V"V8P'  888bod8P' `Y8bod8P'  `Y8bood8P'  8""88888P'        `8'
                                                888                                                                                                
                                               o888o                                                                                               
# ---------------------------------------------
'''
# LEGEND : 
# 0 = CustomerID
# 1 = FirstName
# 2 = MI
# 3 = LastName
# 4 = Address
# 5 = City
# 6 = State
# 7 = Zip
# 8 = SCF
# 9 = Phone
# 10 = Email
# 11 = VIN
# 12 = TradeYear
# 13 = TradeMake
# 14 = TradeModel
# 15 = DelDate
# 16 = Date
# 17 = Radius
# 18 = Dupe1
# 19 = Dupe2
# 20 = Dupe3
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
InputFile = "MergeFile.csv" 
CleanOutput = "/Users/rssenar/Desktop/_CleanOutputPP.csv"
Dupes = "/Users/rssenar/Desktop/_DupesPP.csv" 
# ---------------------------------------------
'''
Select Dedupe Criteria : 
OPHH = One Record Per House Hold
OPP = One Record Per Person
VIN = Vin#
'''
Selection = 'OPHH'
# ---------------------------------------------
FName = 1
LName = 3
Address = 4
Zip = 7
VIN = 11
Entries = set()
# ----------------------------------------------
# Objects
# ----------------------------------------------
Input = csv.reader(open(InputFile,'r'))
OutputClean = csv.writer(open(CleanOutput,'a'))
OutDupes = csv.writer(open(Dupes,'a'))
OutputClean.writerow(['CustomerID','FirstName','MI','LastName','Address','City','State','Zip','SCF',\
	'Phone','Email','VIN','TradeYear','TradeMake','TradeModel','DelDate','Date','Radius','Dupe1','Dupe2','Dupe3'])
OutDupes.writerow(['CustomerID','FirstName','MI','LastName','Address','City','State','Zip','SCF',\
	'Phone','Email','VIN','TradeYear','TradeMake','TradeModel','DelDate','Date','Radius','Dupe1','Dupe2','Dupe3'])
# ----------------------------------------------
# Main Program
# ----------------------------------------------
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		if Selection == 'OPHH':
			key = (line[Address],line[Zip])
			if key not in Entries:
				OutputClean.writerow(line)
				Entries.add(key)
			else:
				OutDupes.writerow(line)
		elif Selection == 'OPP':
			key = (line[FName],line[LName],line[Address],line[Zip])
			if key not in Entries:
				OutputClean.writerow(line)
				Entries.add(key)
			else:
				OutDupes.writerow(line)
		else:
			key = (line[VIN])
			if key not in Entries:
				OutputClean.writerow(line)
				Entries.add(key)
			else:
				OutDupes.writerow(line)

