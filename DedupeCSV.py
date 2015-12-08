'''
  ____           _                   ____ ______     __
 |  _ \  ___  __| |_   _ _ __   ___ / ___/ ___\ \   / /
 | | | |/ _ \/ _` | | | | '_ \ / _ | |   \___ \\ \ / / 
 | |_| |  __| (_| | |_| | |_) |  __| |___ ___) |\ V /  
 |____/ \___|\__,_|\__,_| .__/ \___|\____|____/  \_/   
                        |_|                            
                      
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
InputFileName = input("Enter Suppression File Name : ")
InputFile = "/Users/rssenar/Dropbox/HUB/_PROCESS Folder/" + InputFileName + ".csv"
SuppressionFileName = input("Enter Suppression File Name : ")
SuppressionFile = "/Users/rssenar/Dropbox/HUB/_PROCESS Folder/" + SuppressionFileName + ".csv"
CentralZip = input("Enter Central ZIP codes: ")
# ---------------------------------------------
ZipCoordinateFile = "/Users/rssenar/Dropbox/HUB/py_projects/_Resources/US_ZIP_Coordinates.csv"
# ---------------------------------------------
CleanOutput = "/Users/rssenar/Dropbox/HUB/_PROCESS Folder/__CleanOutput.csv"
CleanOutputDatabase = "/Users/rssenar/Dropbox/HUB/_PROCESS Folder/__CleanOutputDatabase.csv"
CleanOutputPurchase = "/Users/rssenar/Dropbox/HUB/_PROCESS Folder/__CleanOutputPurchase.csv"
Dupes = "/Users/rssenar/Dropbox/HUB/_PROCESS Folder/__Dupes.csv" 
# ---------------------------------------------
# Dedupe Criteria : 
# OPHH = One Record Per House Hold / OPP = One Record Per Person / VIN = Vin#
# ---------------------------------------------
Selection = 'OPHH'
# ---------------------------------------------
CustomerID = 0
FirstName = 1
MI = 2
LastName = 3
Address1 = 4
Address2 = 5
AddressCombined = 6
City = 7
State = 8
Zip = 9
Zip4 = 10
SCF = 11
Phone = 12
Email = 13
VIN = 14
Year = 15
Make = 16
Model = 17
Radius = 20
Coordinates = 21
VINLen = 22
DSF_WALK_SEQ = 23
CRRT = 24
BuybackValues = 26
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

Entries = set()
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
	'Year',\
	'Make',\
	'Model',\
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
HeaderRowDatabase = [\
	'Customer ID',\
	'First Name',\
	'Last Name',\
	'Address',\
	'City',\
	'State',\
	'Zip',\
	'Phone',\
	'Year',\
	'Make',\
	'Model',\
	'Buyback Value',\
	'Winning Number'\
	]
HeaderRowPurchase = [\
	'Customer ID',\
	'First Name',\
	'Last Name',\
	'Address',\
	'City',\
	'State',\
	'Zip',\
	'4Zip',\
	'DSF_WALK_SEQ',\
	'Phone',\
	'Crrt',\
	'Winning Number'\
	]
# ---------------------------------------------
# OBJECTS
# ---------------------------------------------
Input = csv.reader(open(InputFile,'r')) 
ZipCoordinate = csv.reader(open(ZipCoordinateFile,'r'))
OutputClean = csv.writer(open(CleanOutput,'a'))
OutputCleanDatabase = csv.writer(open(CleanOutputDatabase,'a'))
OutputCleanPurchase = csv.writer(open(CleanOutputPurchase,'a'))
OutDupes = csv.writer(open(Dupes,'a'))
OutputClean.writerow(HeaderRow)
OutputCleanDatabase.writerow(HeaderRowDatabase)
OutputCleanPurchase.writerow(HeaderRowPurchase)
OutDupes.writerow(HeaderRow)
# ---------------------------------------------
# ADD SUPPRESSIONS INTO THE ENTRIES SET
# ---------------------------------------------
if SuppressionFileName == "":
	pass
else:
	Suppression = csv.reader(open(SuppressionFile,'r'))
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
	if len(line[MI]) == 1:
		line[MI] = str.upper(line[MI]) 
	else:
		line[MI] = str.title(line[MI]) 
	line[LastName] = str.title(line[LastName])
	line[Address1] = str.title(line[Address1])
	line[Address2] = str.title(line[Address2])
	line[City] = str.title(line[City])
	line[Year] = str.title(line[Year])
	line[Make] = str.title(line[Make])
	line[Model] = str.title(line[Model])
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
		OutputCleanDatabase.writerow((\
			line[CustomerID],\
			line[FirstName],\
			line[LastName],\
			line[AddressCombined],\
			line[City],\
			line[State],\
			line[Zip],\
			line[Phone],\
			line[Year],\
			line[Make],\
			line[Model],\
			line[BuybackValues],\
			line[WinningNum]\
			))
		OutputCleanPurchase.writerow((\
			line[CustomerID],\
			line[FirstName],\
			line[LastName],\
			line[AddressCombined],\
			line[City],\
			line[State],\
			line[Zip],\
			line[Zip4],\
			line[DSF_WALK_SEQ],\
			line[Phone],\
			line[CRRT],\
			line[WinningNum]\
			))
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
		CombineAddress()
		CalculateRadiusfromCentralZip()
		SetCase()
		SetVINLen()
		SetWinningNum()
		SetSCF()
		CheckMailDNQ()
		CheckBlitzDNQ()
		CheckDupeCriteriaThenOutput()
