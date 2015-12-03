'''
 /$$$$$$$                /$$                            /$$$$$$  /$$$$$$ /$$    /$$
| $$__  $$              | $$                           /$$__  $$/$$__  $| $$   | $$
| $$  \ $$ /$$$$$$  /$$$$$$$/$$   /$$ /$$$$$$  /$$$$$$| $$  \__| $$  \__| $$   | $$
| $$  | $$/$$__  $$/$$__  $| $$  | $$/$$__  $$/$$__  $| $$     |  $$$$$$|  $$ / $$/
| $$  | $| $$$$$$$| $$  | $| $$  | $| $$  \ $| $$$$$$$| $$      \____  $$\  $$ $$/ 
| $$  | $| $$_____| $$  | $| $$  | $| $$  | $| $$_____| $$    $$/$$  \ $$ \  $$$/  
| $$$$$$$|  $$$$$$|  $$$$$$|  $$$$$$| $$$$$$$|  $$$$$$|  $$$$$$|  $$$$$$/  \  $/   
|_______/ \_______/\_______/\______/| $$____/ \_______/\______/ \______/    \_/    
                                    | $$                                           
                                    | $$                                           
                                    |__/                                            
'''
#!/usr/bin/python3.4.3
# Required Modules
import csv
from geopy.distance import vincenty
# ---------------------------------------------
# GLOBAL VARIABLE
# ---------------------------------------------
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
# ---------------------------------------------
# InputFile = "/Users/rssenar/Desktop/input.csv" 
# SuppressionFile = "/Users/rssenar/Desktop/suppression.csv"
InputFile = "/Users/rssenar/Desktop/" + input("Enter Input File Name : ") + ".csv" 
SuppressionFile = "/Users/rssenar/Desktop/" + input("Enter Suppression File Name : ") + ".csv" 
CentralZip = input("Enter Central ZIP codes: ")
# ---------------------------------------------
ZipCoordinateFile = "/Users/rssenar/Dropbox/HUB/py_projects/_Resources/US_ZIP_Coordinates.csv" 
# ---------------------------------------------
CleanOutput = "/Users/rssenar/Desktop/__CleanOutput.csv"
Dupes = "/Users/rssenar/Desktop/__Dupes.csv" 
# ---------------------------------------------
# Dedupe Criteria : 
# OPHH = One Record Per House Hold
# OPP = One Record Per Person
# VIN = Vin#
# ---------------------------------------------
Selection = 'OPHH'
# ---------------------------------------------
FirstName = 1
LastName = 3
Address1 = 4
Address2 = 5
AddressCombined = 6
City = 7
State = 8
Zip = 9
SCF = 11
Phone = 12
Email = 13
VIN = 14
TradeYear = 15
TradeMake = 16
TradeModel = 17
Radius = 20
Coordinates = 21
VINLen = 22
WinningNum = 27
MailDNQ = 28
BlitzDNQ = 29
## ZIP Code File
ZipCodeCol = 0
ZipRadiusCol = 1
## ZIP Coordinate File
ZipCodeCoordinateCol = 0
LatitudeCoordinateCol = 1
LongitudeCoordinateCol = 2
## Suppression File
SupprAddressCol = 2
SupprZipCol = 5
# ---------------------------------------------
HeaderRow = [\
	'Customer ID',\
	'First Name',\
	'MI',\
	'Last Name',\
	'Address1',\
	'Address2',\
	'Address',\
	'City',\
	'State',\
	'Zip',\
	'4Zip',\
	'SCF',\
	'Phone',\
	'Email',\
	'VIN',\
	'TradeYear',\
	'TradeMake',\
	'TradeModel',\
	'DelDate',\
	'Date',\
	'Radius',\
	'Coordinates',\
	'VINLen',\
	'DSF_WALK_SEQ',\
	'Crrt',\
	'KBB',\
	'Buyback Value',\
	'Winning Number',\
	'Mail DNQ',\
	'Blitz DNQ',\
	'Misc1',\
	'Misc2',\
	'Misc3'\
	]
# ---------------------------------------------
# OBJECTS
# ---------------------------------------------
Input = csv.reader(open(InputFile,'r')) 
ZipCoordinate = csv.reader(open(ZipCoordinateFile,'r'))
Suppression = csv.reader(open(SuppressionFile,'r'))
ZipCoordinateAppend = csv.reader(open(ZipCoordinateFile,'a'))
OutputClean = csv.writer(open(CleanOutput,'a'))
OutDupes = csv.writer(open(Dupes,'a'))
OutputClean.writerow(HeaderRow)
OutDupes.writerow(HeaderRow)
# ---------------------------------------------
# ADD SUPPRESSIONS INTO THE ENTRIES SET
# ---------------------------------------------
Entries = set()
FirstLine = True
for line in Suppression:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		Entries.add((str.title(line[SupprAddressCol]),str.title(line[SupprZipCol])))
# ---------------------------------------------
# LOAD ZIP DICTIONARY INTO MEMORY
# ---------------------------------------------
ZipCoordinateDict = {}
FirstLine = True
for line in ZipCoordinate:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		ZipCoordinateDict[line[ZipCodeCoordinateCol]] = (line[LatitudeCoordinateCol], line[LongitudeCoordinateCol])
# ---------------------------------------------
# FUNCTIONS
# ---------------------------------------------
def CalculateRadiusfromCentralZip():
	if CentralZip in ZipCoordinateDict:
		OriginZipCoordinates = ZipCoordinateDict[CentralZip]
	else:
		OriginZipCoordinates = 0

	if line[Zip] in ZipCoordinateDict:
		TargetZipCoordinates = ZipCoordinateDict[line[Zip]]
		line[Coordinates] = TargetZipCoordinates
	else:
		TargetZipCoordinates = 0

	if OriginZipCoordinates == 0 or TargetZipCoordinates == 0:
		line[Radius] = "n/a"
	else:
		line[Radius] = (float(vincenty(OriginZipCoordinates, TargetZipCoordinates).miles))

def SetCase(): # Set case fields
	line[FirstName] = str.title(line[FirstName]) 
	line[LastName] = str.title(line[LastName])
	line[Address1] = str.title(line[Address1])
	line[Address2] = str.title(line[Address2])
	line[City] = str.title(line[City])
	line[TradeYear] = str.title(line[TradeYear])
	line[TradeMake] = str.title(line[TradeMake])
	line[TradeModel] = str.title(line[TradeModel])
	line[Email] = str.lower(line[Email])
	line[State] = str.upper(line[State])

def SetVINLen(): # Assign the Length of the VIN# to VinLen Field
	line[VINLen] = len(line[VIN])
	if line[VINLen] < 17:
		line[VIN] = ""
	else:
		line[VIN] = str.upper(line[VIN])

def SetWinningNum(): # Assign Winning Number to Winning Number Field
	line[WinningNum] = 40754

def CombineAddress(): # Combine Address 1 & Address 2 fields
	if line[AddressCombined] == "":
		if line[Address2] == "":
			line[AddressCombined] = line[Address1] # If Address2 is empty
		else:
			line[AddressCombined] = line[Address1] + ' ' + line[Address2]
	else:
		line[AddressCombined] = str.title(line[AddressCombined])

def SetSCF(): # Parse VIN# then assign value to SCF field
	ZipLen = len(line[Zip])
	if ZipLen < 5:
		line[SCF] = (line[Zip])[:2] # if ZIP is less than 5 Digits
	else:
		line[SCF] = (line[Zip])[:3] # if ZIP is 5 Digits

def CheckMailDNQ():
	if line[FirstName] == "" or line[LastName] == "":
		line[MailDNQ] = "dnq"
	else:
		line[MailDNQ] = ""

def CheckBlitzDNQ():
	if len(line[Phone]) < 8 or len(line[VIN]) < 17: 
		line[BlitzDNQ] = "dnq"
	else:
		line[BlitzDNQ] = ""

def CheckDupeCriteriaThenOutput(): # Checks Selection Criteria
	if Selection == 'OPHH':
		key = (line[AddressCombined],line[Zip])
	if Selection == 'OPP':
		key = (line[FirstName],line[LastName],line[AddressCombined],line[Zip])
	if Selection == 'VIN':
		key = (line[VIN])
	if key not in Entries: # Check if key is in the Entries set
		OutputClean.writerow(line) # write to processed output file
		Entries.add(key) # add row to Entries set
	else:
		OutDupes.writerow(line) # write to Dupes file
# ---------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		CalculateRadiusfromCentralZip()
		SetCase()
		SetVINLen()
		SetWinningNum()
		SetSCF()
		CombineAddress()
		CheckMailDNQ()
		CheckBlitzDNQ()
		CheckDupeCriteriaThenOutput()
