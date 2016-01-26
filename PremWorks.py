#!/usr/bin/python2.7.10
# ---------------------------------------------
# PREMWORKS PROJECT
# ---------------------------------------------
# Required Modules
# ---------------------------------------------
from __future__ import division, print_function
import csv
from geopy.distance import vincenty
from dateutil.parser import *
from datetime import *
from tqdm import tqdm
# ---------------------------------------------
# GLOBAL VARIABLE
# ---------------------------------------------
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
# ---------------------------------------------
# ---------------------------------------------
ZipCoordinateFile = "/Users/rssenar/Dropbox/HUB/Projects/_Resources/US_ZIP_Coordinates.csv"
YearDecodeFile = "/Users/rssenar/Dropbox/HUB/Projects/_Resources/Year_Decode.csv"
# ---------------------------------------------
InputFileName = raw_input("Enter Name : ")
InputFile = "/Users/rssenar/Desktop/" + InputFileName + ".csv"
SuppressionFileName = raw_input("Enter Suppression Name : ")
SuppressionFile = "/Users/rssenar/Desktop/" + SuppressionFileName + ".csv"
CentralZip = raw_input("Enter Central ZIP codes: ")
# ---------------------------------------------
CleanOutput = "/Users/rssenar/Desktop/__CleanOutputMAIN.csv"
CleanOutputDatabase = "/Users/rssenar/Desktop/_CleanOutputDatabaseFormat.csv"
CleanOutputPurchase = "/Users/rssenar/Desktop/_CleanOutputPurchaseFormat.csv"
Dupes = "/Users/rssenar/Desktop/_DUPES.csv" 
# ---------------------------------------------
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
DelDate = 18
Date = 19
Radius = 20
Coordinates = 21
VINLen = 22
DSF_WALK_SEQ = 23
CRRT = 24
KBB = 25
BuybackValues = 26
WinningNum = 27
MailDNQ = 28
BlitzDNQ = 29
Misc1 = 30
Misc2 = 31
Misc3 = 32

## ZIP Code File
ZipCodeCol = 0
ZipRadiusCol = 1

## ZIP Coordinate File
ZipCodeCoordinateCol = 0
LatitudeCoordinateCol = 1
LongitudeCoordinateCol = 2

## VIN Decode File
YearDecodeYearAb = 0
YearDecodeYear = 1

## Suppression File
SupprAddressCol = 2
SupprZipCol = 5
SupprPhoneCol = 6

## Sets
Entries = set()
## Set Sequence Number
SeqNum = 1000
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
InputFile = open(InputFile,'rb')
ZipCoordinateFile = open(ZipCoordinateFile,'rb')
YearDecodeFile = open(YearDecodeFile,'rb')
CleanOutput = open(CleanOutput,'ab')
CleanOutputDatabase = open(CleanOutputDatabase,'ab')
CleanOutputPurchase = open(CleanOutputPurchase,'ab')
Dupes = open(Dupes,'ab')
# ---------------------------------------------
Input = csv.reader(InputFile)
ZipCoordinate = csv.reader(ZipCoordinateFile)
YearDecode = csv.reader(YearDecodeFile)
OutputClean = csv.writer(CleanOutput)
OutputCleanDatabase = csv.writer(CleanOutputDatabase)
OutputCleanPurchase = csv.writer(CleanOutputPurchase)
OutDupes = csv.writer(Dupes)
# ---------------------------------------------
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
	SuppressionFile = open(SuppressionFile,'r')
	Suppression = csv.reader(SuppressionFile)
	FirstLine = True
	for line in Suppression:
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			Entries.add((str.title(line[SupprAddressCol]),str.title(line[SupprZipCol])))
	SuppressionFile.close()
# ---------------------------------------------
# LOAD ZIP DICT INTO MEMORY
# ---------------------------------------------
ZipCoordinateDict = {}
FirstLine = True
for line in ZipCoordinate:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		ZipCoordinateDict[line[ZipCodeCoordinateCol]] = (line[LatitudeCoordinateCol], line[LongitudeCoordinateCol])
# ---------------------------------------------
# LOAD YEAR DECODE DICT INTO MEMORY
# ---------------------------------------------
YearDecodeDict = {}
FirstLine = True
for line in YearDecode:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		YearDecodeDict[line[YearDecodeYearAb]] = (line[YearDecodeYear])
# ---------------------------------------------
# FUNCTIONS
# ---------------------------------------------
def SetCustomerID():
	if line[DSF_WALK_SEQ] == '':
		line[CustomerID] = 'd' + str(SeqNum)
	else:
		line[CustomerID] = 'a' + str(SeqNum)

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

def YearDecode():
	if str(line[Year]) in YearDecodeDict:
		line[Misc1] = YearDecodeDict[line[Year]]
	else:
		line[Misc1] = ''

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

def SetVINLen(): 
	line[VINLen] = len(line[VIN])
	if line[VINLen] < 17:
		line[VIN] = ""
	else:
		line[VIN] = str.upper(line[VIN])

def SetDateFormat():
	CurrentDate = parse('')
	CurrentDateUpdate = CurrentDate.date()
	
	DelDateNew = parse(line[DelDate])
	DelDateUpdate = DelDateNew.date()

	DateNew = parse(line[Date])
	DateUpdate = DateNew.date()

	if DelDateUpdate == CurrentDateUpdate:
		line[DelDate] = ''
	else:
		line[DelDate] = DelDateUpdate

	if DateUpdate == CurrentDateUpdate:
		line[Date] = ''
	else:
		line[Date] = DateUpdate

def SetWinningNum(): 
	line[WinningNum] = 40754

def CombineAddress(): 
	if line[AddressCombined] == "":
		if line[Address2] == "":
			line[AddressCombined] = line[Address1] 
		else:
			line[AddressCombined] = line[Address1] + ' ' + line[Address2]
	else:
		line[AddressCombined] = str.title(line[AddressCombined])

def SetSCF(): 
	ZipLen = len(line[Zip])
	if ZipLen < 5:
		line[SCF] = (line[Zip])[:2] 
	else:
		line[SCF] = (line[Zip])[:3] 

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

def CheckDupeCriteriaThenOutput(): 
	if Selection == 'OPHH':
		key = (line[AddressCombined],line[Zip])
	if Selection == 'OPP':
		key = (line[FirstName],line[LastName],line[AddressCombined],line[Zip])
	if Selection == 'VIN':
		key = (line[VIN])
	if Selection == 'PHONE':
		key = (line[Phone])
	if key not in Entries:
		Entries.add(key)
		OutputClean.writerow(line)
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
	else:
		OutDupes.writerow(line)
# ---------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------
FirstLine = True
for line in tqdm(Input):
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		SetCustomerID()
		SetCase()
		CombineAddress()
		CalculateRadiusfromCentralZip()
		YearDecode()
		SetVINLen()
		SetDateFormat()
		SetWinningNum()
		SetSCF()
		CheckMailDNQ()
		CheckBlitzDNQ()
		CheckDupeCriteriaThenOutput()
	SeqNum += 1
# ---------------------------------------------
# Close OBJECTS
# ---------------------------------------------
InputFile.close()
ZipCoordinateFile.close()
YearDecodeFile.close()
CleanOutput.close()
CleanOutputDatabase.close()
CleanOutputPurchase.close()
Dupes.close()
