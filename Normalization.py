#!/usr/bin/env python
# ---------------------------------------------
'''
Import required modules
'''
from __future__ import division, print_function
import csv, os
from geopy.distance import vincenty
from dateutil.parser import *
from datetime import *
from tqdm import tqdm
# ---------------------------------------------
'''
Set TRUE or FALSE value depending if input files include a header row
'''
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
DatabaseHeader =  True
DatabaseFirstLine = True
PurchaseHeader =  True
PurchaseFirstLine = True
PhonesHeader =  True
PhonesFirstLine = True
# ---------------------------------------------
ZipCoordFile = "../_Resources/US_ZIP_Coordinates.csv"
YearDecodeFile = "../_Resources/Year_Decode.csv"
GenSuppressionFile = "../_Resources/Gen_Suppression_File.csv"
DropFile = "../_Resources/Drop_File.csv"
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
CleanOutputPhones = "../../../../Desktop/" + "_" + InputFileName + " PHONES.csv"
Dupes = "../../../../Desktop/__DUPLICATES.csv" 
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
ZipCRRT = 25 
KBB = 26
BuybackValues = 27
WinningNum = 28
MailDNQ = 29
BlitzDNQ = 30
DropVal = 31
Misc1 = 32
Misc2 = 33
Misc3 = 34

Entries = set()
SeqNum = 10000
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
	'ZipCrrt',\
	'KBB',\
	'Buyback Value',\
	'Winning Number',\
	'Mail DNQ',\
	'Blitz DNQ',\
	'Drop',\
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
	'Winning Number',\
	'Drop'\
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
	'Winning Number',\
	'Drop'\
	]
HeaderRowPhones = [\
	'First Name',\
	'Last Name',\
	'Phone',\
	'Address',\
	'City',\
	'State',\
	'Zip'\
	]
# ---------------------------------------------
'''
Create Objects and csv.reader and csv.writer methods
'''
InputFile = open(InputFile,'rU')
Input = csv.reader(InputFile)
# ---------------------------------------------
GenSuppressionFile = open(GenSuppressionFile,'rU')
GenSuppression = csv.reader(GenSuppressionFile)
# ---------------------------------------------
CleanOutput = open(CleanOutput,'ab')
OutputClean = csv.writer(CleanOutput)
OutputClean.writerow(HeaderRow)
# ---------------------------------------------
Dupes = open(Dupes,'ab')
OutDupes = csv.writer(Dupes)
OutDupes.writerow(HeaderRow)
# ---------------------------------------------
# CleanOutputDatabase = open(CleanOutputDatabase,'ab')
# CleanOutputPurchase = open(CleanOutputPurchase,'ab')
# CleanOutputPhones = open(CleanOutputPhones,'ab')
# Dupes = open(Dupes,'ab')
# ---------------------------------------------
'''
Add SPECIFIC Suppression File values (If Specified) into the entries set for the purposes of de-duping
'''
if SuppressionFileName == "":
	pass
else:
	SuppressionFile = open(SuppressionFile,'rU')
	Suppression = csv.reader(SuppressionFile)
	FirstLine = True
	for line in Suppression:
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			Entries.add((str.title(line[2]),str.title(line[5])))
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
		Entries.add((str.title(line[2]),str.title(line[5])))
# ---------------------------------------------
'''
Create a Zip Dictionary from US_ZIP_Coordinates.csv file and load into
memory. Information includes Longitude and Latitude Information
'''
ZipCoordinateDict = {}
ZipCoordFile = open(ZipCoordFile,'rU')
ZipCoordinate = csv.reader(ZipCoordFile)
FirstLine = True
for line in ZipCoordinate:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		ZipCoordinateDict[line[0]] = (line[1], line[2])
ZipCoordFile.close()
# ---------------------------------------------
'''
Create a Drop Dictionary from Drop_File.csv file
'''
DropDict = {}
DropFile = open(DropFile,'rU')
Drop = csv.reader(DropFile)
FirstLine = True
for line in Drop:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		DropDict[line[0]] = line[1]
DropFile.close()
# ---------------------------------------------
'''
Create a Year Decode Dictionary from Year_Decode.csv file and load into
memory
'''
YearDecodeDict = {}
YearDecodeFile = open(YearDecodeFile,'rU')
YearDecode = csv.reader(YearDecodeFile)
FirstLine = True
for line in YearDecode:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		YearDecodeDict[line[0]] = (line[1])
YearDecodeFile.close()
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
def SetCase():
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
		line
		line[SCF] = (line[Zip])[:2] 
	else:
		line[SCF] = (line[Zip])[:3] 
''' 
Fuction combined Zip + Crrt Fields
'''
def SetZipCrrt(): 
	if line[Zip] == '' or line[CRRT] == '':
		line[ZipCRRT] = ''
	else:
		line[ZipCRRT] = line[Zip] + line[CRRT]
''' 
Fuction Sets DROP Number
'''
def SetDrop():
	if line[DSF_WALK_SEQ] == '':
		if line[Zip] in DropDict:
			line[DropVal] = DropDict[line[Zip]]
		else:
			line[DropVal] = ''
	else:
		if line[ZipCRRT] in DropDict:
			line[DropVal] = DropDict[line[ZipCRRT]]
		else:
			line[DropVal] = ''
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
Function checks for dupes based on: OPHH = One Record Per House Hold, 
OPP = One Record Per Person or VIN = Vin#
'''
def CheckDupeCriteriaThenOutput(): 
	key = (line[AddressComb],line[Zip])
	# key = (line[FirstName],line[LastName],line[AddressComb],line[Zip])
	# key = (line[VIN])
	if key not in Entries:
		Entries.add(key)
		OutputClean.writerow(line)
	else:
		OutDupes.writerow(line)
'''
Function outputs processed Database, Purchase & Dupes Files
'''
def CreateDatabasePurchaseOutput():
	global DatabaseFirstLine
	global PurchaseFirstLine
	global CleanOutputDatabase
	global CleanOutputPurchase
	if line[DSF_WALK_SEQ] == '':
		if DatabaseHeader and DatabaseFirstLine:
			CleanOutputDatabase = open(CleanOutputDatabase,'ab')
			OutputCleanDatabase = csv.writer(CleanOutputDatabase)
			OutputCleanDatabase.writerow(HeaderRowDatabase)
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
				line[WinningNum],\
				line[DropVal]\
				))
			DatabaseFirstLine = False
		else:
			OutputCleanDatabase = csv.writer(CleanOutputDatabase)
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
				line[WinningNum],\
				line[DropVal]\
				))
	else:
		if PurchaseHeader and PurchaseFirstLine:
			CleanOutputPurchase = open(CleanOutputPurchase,'ab')
			OutputCleanPurchase = csv.writer(CleanOutputPurchase)
			OutputCleanPurchase.writerow(HeaderRowPurchase)
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
				line[WinningNum],\
				line[DropVal]\
				))
			PurchaseFirstLine = False
		else:
			OutputCleanPurchase = csv.writer(CleanOutputPurchase)
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
				line[WinningNum],\
				line[DropVal]\
				))

'''
Function outputs Phone List File
'''
def ExtractPhonesList():
	global PhonesFirstLine
	global CleanOutputPhones
	if line[Phone] != '':
		if PhonesHeader and PhonesFirstLine:
			CleanOutputPhones = open(CleanOutputPhones,'ab')
			OutputPhones = csv.writer(CleanOutputPhones)
			OutputPhones.writerow(HeaderRowPhones)
			OutputPhones.writerow((\
				line[FirstName],\
				line[LastName],\
				line[Phone],\
				line[AddressComb],\
				line[City],\
				line[State],\
				line[Zip]\
				))
			PhonesFirstLine = False
		else:
			OutputPhones = csv.writer(CleanOutputPhones)
			OutputPhones.writerow((\
				line[FirstName],\
				line[LastName],\
				line[Phone],\
				line[AddressComb],\
				line[City],\
				line[State],\
				line[Zip]\
				))

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
		SetZipCrrt()
		# SetDrop()
		CheckMailDNQ()
		CheckBlitzDNQ()
		CheckDupeCriteriaThenOutput()
		CreateDatabasePurchaseOutput()
		ExtractPhonesList()
	SeqNum+=1
# ---------------------------------------------
''' 
Close all opened objects
'''
InputFile.close()
CleanOutput.close()
GenSuppressionFile.close()
Dupes.close()
if line[DSF_WALK_SEQ] == '':
	CleanOutputDatabase.close()
else:
	CleanOutputPurchase.close()
if line[Phone] != '':
	CleanOutputPhones.close()
# ---------------------------------------------