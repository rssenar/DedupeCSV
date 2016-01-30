#!/usr/bin/env python
# ---------------------------------------------
'''
Import required modules
'''
from __future__ import division, print_function
import csv
from geopy.distance import vincenty
from dateutil.parser import *
from datetime import *
from tqdm import tqdm
# ---------------------------------------------
'''
Set TRUE or FALSE value depending if input files include a header row
'''
CSVFilesHaveHeaderRow = True
# ---------------------------------------------
ZipCoordFile = "../_Resources/US_ZIP_Coordinates.csv"
YearDecodeFile = "../_Resources/Year_Decode.csv"
GenSuppressionFile = "../_Resources/Gen_Suppression_File.csv"
# ---------------------------------------------
InputFileName = raw_input("Enter Name : ")
InputFile = "../../../../Desktop/" + InputFileName + ".csv"
SuppressionFileName = raw_input("Enter Suppression Name : ")
SuppressionFile = "../../../../Desktop/" + SuppressionFileName + ".csv"
CentralZip = raw_input("Enter Central ZIP codes: ")
# ---------------------------------------------
CleanOutput = "../../../../Desktop/" + "__" + InputFileName + "_CleanOutputMAIN.csv"
CleanOutputDatabase = "../../../../Desktop/" + "_" + InputFileName + " UPLOAD DATA.csv"
CleanOutputPurchase = "../../../../Desktop/" + "_" + InputFileName + " UPLOAD.csv"
Dupes = "../../../../Desktop/_DUPLICATES.csv" 
# ---------------------------------------------
'''
Set selection options:
OPHH = One Record Per House Hold
OPP = One Record Per Person
VIN = Vin#
'''
Selection = 'OPHH'
# ---------------------------------------------
'''
Assign list numbers to variables for readability
'''
CustomerID = 0
FirstName = 1
MI = 2
LastName = 3
Address1 = 4
Address2 = 5
AddressComb = 6
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
# ZIPCode File
ZipCodeCol = 0
ZipRadiusCol = 1
# ZIPCoordinate File
ZipCoordCol = 0
LatCoordCol = 1
LongCoordCol = 2
# VINDecode File
YearDecodeYearAb = 0
YearDecodeYear = 1
# Suppression File
SupprAddressCol = 2
SupprZipCol = 5
# GenSuppression File
GenSupprAddressCol = 2
GenSupprZipCol = 5
# Set
Entries = set()
# Set Sequence#
SeqNum = 1000
# ---------------------------------------------
'''
Assign column names to header output files
'''
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
	#'Year',\
	#'Make',\
	#'Model',\
	#'Buyback Value',\
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
	#'Phone',\
	'Crrt',\
	'Winning Number'\
	]
# ---------------------------------------------
'''
Create Objects and csv.reader and csv.writer methods
'''
InputFile = open(InputFile,'rb')
ZipCoordFile = open(ZipCoordFile,'rb')
YearDecodeFile = open(YearDecodeFile,'rb')
GenSuppressionFile = open(GenSuppressionFile,'rb')
CleanOutput = open(CleanOutput,'ab')
CleanOutputDatabase = open(CleanOutputDatabase,'ab')
CleanOutputPurchase = open(CleanOutputPurchase,'ab')
Dupes = open(Dupes,'ab')
# ---------------------------------------------
Input = csv.reader(InputFile)
ZipCoordinate = csv.reader(ZipCoordFile)
YearDecode = csv.reader(YearDecodeFile)
GenSuppression = csv.reader(GenSuppressionFile)
OutputClean = csv.writer(CleanOutput)
OutputCleanDatabase = csv.writer(CleanOutputDatabase)
OutputCleanPurchase = csv.writer(CleanOutputPurchase)
OutDupes = csv.writer(Dupes)
# ---------------------------------------------
'''
Create output files and assign headers to header row
'''
OutputClean.writerow(HeaderRow)
OutputCleanDatabase.writerow(HeaderRowDatabase)
OutputCleanPurchase.writerow(HeaderRowPurchase)
OutDupes.writerow(HeaderRow)
# ---------------------------------------------
'''
Add SPECIFIC Suppression File values (If Specified) into the entries set for the purposes of de-duping
'''
if SuppressionFileName == "":
	pass
else:
	SuppressionFile = open(SuppressionFile,'rb')
	Suppression = csv.reader(SuppressionFile)
	FirstLine = True
	for line in Suppression:
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			Entries.add((str.title(line[SupprAddressCol]),str.title(line[SupprZipCol])))
	SuppressionFile.close()
# ---------------------------------------------
'''
Add GENERAL Suppression File values into the entries set for the purposes of de-duping
'''
FirstLine = True
for line in GenSuppression:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		Entries.add((str.title(line[GenSupprAddressCol]),str.title(line[GenSupprZipCol])))
# ---------------------------------------------
'''
Create a Zip Dictionary from US_ZIP_Coordinates.csv file and load into
memory. Information includes Longitude and Latitude Information
'''
ZipCoordinateDict = {}
FirstLine = True
for line in ZipCoordinate:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		ZipCoordinateDict[line[ZipCoordCol]] = (line[LatCoordCol], line[LongCoordCol])
# ---------------------------------------------
'''
Create a Year Decode Dictionary from Year_Decode.csv file and load into
memory
'''
YearDecodeDict = {}
FirstLine = True
for line in YearDecode:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		YearDecodeDict[line[YearDecodeYearAb]] = (line[YearDecodeYear])
# ---------------------------------------------
# Fuctions
# ---------------------------------------------
''' 
Function sets Customer ID Sequence Number.  If walk sequence is not present,
assig "d" to sequence number. else, set "a"
'''
def SetCustomerID():
	if line[DSF_WALK_SEQ] == '':
		line[CustomerID] = 'd' + str(SeqNum)
	else:
		line[CustomerID] = 'a' + str(SeqNum)

''' 
Function calculates the radius based on the central zip specified. Distance
is calculated by the vincenty method from the geopy module
'''
def CalculateRadiusfromCentralZip():
	if CentralZip in ZipCoordinateDict:
		OriginZipCoord = ZipCoordinateDict[CentralZip]
	else:
		OriginZipCoord = 0

	if line[Zip] in ZipCoordinateDict:
		TargetZipCoord = ZipCoordinateDict[line[Zip]]
		line[Coordinates] = TargetZipCoord
	else:
		TargetZipCoord = 0

	if OriginZipCoord == 0 or TargetZipCoord == 0:
		line[Radius] = "n/a"
	else:
		line[Radius] = (float(vincenty(OriginZipCoord, TargetZipCoord).miles))

''' 
Function decodes the year column if year is abreviated to 2 digits. e.g 
2015 = 15 or 2007 = 7
'''
def YearDecode():
	if str(line[Year]) in YearDecodeDict:
		line[Misc1] = YearDecodeDict[line[Year]]
	else:
		line[Misc1] = ''

''' 
Function sets case for FirstName, MI, LastName, Address1, Address2, City,
Year, Make, Model, Year, Email & State to Title Case for better readability
'''
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

''' 
Fuction deletes VIN if VIN length is less than the standard 17 characters
'''
def SetVINLen(): 
	line[VINLen] = len(line[VIN])
	if line[VINLen] < 17:
		line[VIN] = ""
	else:
		line[VIN] = str.upper(line[VIN])

''' 
Fuction normalizes the date column
'''
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

''' 
Fuction sets the value for the winning # column
'''
def SetWinningNum(): 
	line[WinningNum] = 40754

''' 
Fuction combines values for Address1 & Address2
'''
def CombineAddress(): 
	if line[AddressComb] == "":
		if line[Address2] == "":
			line[AddressComb] = line[Address1] 
		else:
			line[AddressComb] = line[Address1] + ' ' + line[Address2]
	else:
		line[AddressComb] = str.title(line[AddressComb])

''' 
Fuction extrapolates 3-Digit SCF from the ZIP code
'''
def SetSCF(): 
	ZipLen = len(line[Zip])
	if ZipLen < 5:
		line[SCF] = (line[Zip])[:2] 
	else:
		line[SCF] = (line[Zip])[:3] 

''' 
Fuction assigns 'dnq' to records that dont qualify for mail
'''
def CheckMailDNQ():
	if line[FirstName] == "" or line[LastName] == "":
		line[MailDNQ] = "dnq"
	else:
		line[MailDNQ] = ""

''' 
Fuction assigns 'dnq' to records that dont qualify for phone blitz
'''
def CheckBlitzDNQ():
	if len(line[Phone]) < 8 or len(line[VIN]) < 17: 
		line[BlitzDNQ] = "dnq"
	else:
		line[BlitzDNQ] = ""

'''
Fuction checks for dupes based on:
OPHH = One Record Per House Hold
OPP = One Record Per Person
VIN = Vin#
Value is then added to 'Entries' set to avoid dedupe
'''
def CheckDupeCriteriaThenOutput(): 
	if Selection == 'OPHH':
		key = (line[AddressComb],line[Zip])
	if Selection == 'OPP':
		key = (line[FirstName],line[LastName],line[AddressComb],line[Zip])
	if Selection == 'VIN':
		key = (line[VIN])
	if key not in Entries:
		Entries.add(key)
		OutputClean.writerow(line)
		OutputCleanDatabase.writerow((\
			line[CustomerID],\
			line[FirstName],\
			line[LastName],\
			line[AddressComb],\
			line[City],\
			line[State],\
			line[Zip],\
			line[Phone],\
			#line[Year],\
			#line[Make],\
			#line[Model],\
			#line[BuybackValues],\
			line[WinningNum]\
			))
		OutputCleanPurchase.writerow((\
			line[CustomerID],\
			line[FirstName],\
			line[LastName],\
			line[AddressComb],\
			line[City],\
			line[State],\
			line[Zip],\
			line[Zip4],\
			line[DSF_WALK_SEQ],\
			#line[Phone],\
			line[CRRT],\
			line[WinningNum]\
			))
	else:
		OutDupes.writerow(line)
# ---------------------------------------------
# Main Program
# ---------------------------------------------
''' 
If set to TRUE, 1st record of CSV file will be skipped. If set to FALSE,
1st record of CSV file will be included.  
'''
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
''' 
Close all opened objects
'''
InputFile.close()
ZipCoordFile.close()
YearDecodeFile.close()
CleanOutput.close()
CleanOutputDatabase.close()
CleanOutputPurchase.close()
Dupes.close()
GenSuppressionFile.close()