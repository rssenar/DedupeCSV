
#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, re
import pandas as pd
from geopy.distance import vincenty
from dateutil.parser import *
from datetime import *
from tqdm import tqdm
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
CleanOutputFirstTime = True
DatabaseFirstTime = True
PurchaseFirstTime = True
PurchaseFirstTimeP = True
PurchaseFirstTimeN = True
PurchaseFirstTimeAll = True
PhonesFirstTime = True
DupesFirstTime = True
AppendFirstTime = True
AppendFirstTimeP = True
AppendFirstTimeN = True
MDNQFirstTime = True
# ---------------------------------------------
ZipCoordFile = '../Dropbox/HUB/Projects/_Resources/US_ZIP_Coordinates.csv'
YearDecodeFile = '../Dropbox/HUB/Projects/_Resources/Year_Decode.csv'
GenSuppressionFile = '../Dropbox/HUB/Projects/_Resources/GEN_Suppression.csv'
DropFile = '../Dropbox/HUB/Projects/_Resources/Drop_File.csv'
# ---------------------------------------------
WinningNumber = 40754
SeqNumDatabase = 10000
SeqNumPurchaseP = 30000
SeqNumPurchaseN = 40000
SeqNumPurchase = 50000
Entries = set()
# ---------------------------------------------
IPFName = raw_input('Enter Name : ')
InputFile = IPFName + '.csv'
# ---------------------------------------------
# Import Zip Dictionary from US_ZIP_Coordinates.csv file
ZipCoordinateDict = {}
with open(ZipCoordFile,'rU') as ZipCoordFile:
	ZipCoordinate = csv.reader(ZipCoordFile)
	FirstLine = True
	for line in ZipCoordinate:
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			ZipCoordinateDict[line[0]] = (line[1], line[2])
# ---------------------------------------------
# Import LOCAL Suppression File for the purposes of de-duping
SuppressionFileName = raw_input('Enter Suppression Name : ')
SuppressionFile = SuppressionFileName+'.csv'
if SuppressionFileName != '':
	with open(SuppressionFile,'rU') as SuppressionFile:
		Suppression = csv.reader(SuppressionFile)
		FirstLine = True
		for line in Suppression:
			if CSVFilesHaveHeaderRow and FirstLine:
				FirstLine = False
			else:
				Entries.add((str.title(line[2]),str.title(line[5])))
# ---------------------------------------------
# Import GENERAL Suppression File for the purposes of de-duping
with open(GenSuppressionFile,'rU') as GenSuppressionFile:
	GenSuppression = csv.reader(GenSuppressionFile)
	FirstLine = True
	for line in GenSuppression:
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			Entries.add((str.title(line[2]),str.title(line[5])))
# ---------------------------------------------
# Import Drop Dictionary from Drop_File.csv file
DropDict = {}
with open(DropFile,'rU') as DropFile:
	Drop = csv.reader(DropFile)
	FirstLine = True
	for line in Drop:
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			DropDict[line[0]] = line[1]
# ---------------------------------------------
# Import Year Decode Dictionary from Year_Decode.csv file
YearDecodeDict = {}
with open(YearDecodeFile,'rU') as YearDecodeFile:
	YearDecode = csv.reader(YearDecodeFile)
	FirstLine = True
	for line in YearDecode:
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			YearDecodeDict[line[0]] = (line[1])
# ---------------------------------------------
CentralZip = raw_input('Enter Central ZIP codes: ')
while CentralZip not in ZipCoordinateDict:
	CentralZip = raw_input('Invalid Zip code, Enter Central ZIP Codes: ')
# ---------------------------------------------
HRSelect = raw_input('Re-Map Header Row? [Y/N]: ')
while HRSelect != 'Y' and HRSelect != 'y' and \
HRSelect != 'N' and HRSelect != 'n':
	HRSelect = raw_input('Invalid entry, Re-Map Header Row? [Y/N]: ')
# ---------------------------------------------
CleanOutput = IPFName + '_OutputMASTER.csv'
CleanOutputPD = IPFName + '_OutputMASTER.csv'
# ---------------------------------------------
ReMappedOutput = '<<<< ' + IPFName + '_Re-Mapped.csv'
Dupes = '<<<< DUPES.csv'
MDNQ = '<<<< MAIL-DNQ.csv'
# ---------------------------------------------
CleanOutputPurchaseP = '<< ' + IPFName + '_Penny.csv'
CleanOutputPurchaseN = '<< ' + IPFName + '_Nickel.csv'
CleanOutputPurchaseR = '<< ' + IPFName + '_Other.csv'
# ---------------------------------------------
CleanOutputDatabase = IPFName + '_UPLOAD-DATA.csv'
CleanOutputPurchaseAll = IPFName + '_UPLOAD.csv'
CleanOutputAppend = IPFName + '_MAIN List.csv'
CleanOutputAppendP = IPFName + '_PENNY List.csv'
CleanOutputAppendN = IPFName + '_NICKEL List.csv'
CleanOutputPhones = IPFName + '_PHONES List.csv'
# ---------------------------------------------
# Assign Variables For Readability
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
HPhone = 13
WPhone = 14
MPhone = 15
Email = 16
VIN = 17
Year = 18
Make = 19
Model = 20
DelDate = 21
Date = 22
Radius = 23
Coordinates = 24
VINLen = 25
DSF_WALK_SEQ = 26
CRRT = 27
ZipCRRT = 28
KBB = 29
BuybackValues = 30
WinningNum = 31
MailDNQ = 32
BlitzDNQ = 33
DropVal = 34
PURL = 35
Misc1 = 36
Misc2 = 37
Misc3 = 38

# Assign Column Names To Header Output Files
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
	'HPH',\
	'BPH',\
	'CPH',\
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
	'PURL',\
	'Misc1',\
	'Misc2',\
	'Misc3'\
	]
# ---------------------------------------------
# Re-Map Column Fields
def ReMapHeaderFields():
	HeaderDict = {}
	def match(field):
		if bool(re.search('cus.+id',field,flags=re.I)):
			HeaderDict[CustomerID] = 'line['+str(i)+']'
		elif bool(re.search('fir.+me',field,flags=re.I)):
			HeaderDict[FirstName] = 'line['+str(i)+']'
		elif bool(re.search(r'\bmi\b',field,flags=re.I)) or\
			bool(re.search(r'\bmiddle\b',field,flags=re.I)):
			HeaderDict[MI] = 'line['+str(i)+']' 
		elif bool(re.search('las.+me',field,flags=re.I)):
			HeaderDict[LastName] = 'line['+str(i)+']' 
		elif bool(re.search('.ddr.+1',field,flags=re.I)):
			HeaderDict[Address1] = 'line['+str(i)+']' 
		elif bool(re.search('.ddr.+2',field,flags=re.I)):
			HeaderDict[Address2] = 'line['+str(i)+']' 
		elif bool(re.search('.ddr.+',field,flags=re.I)):
			HeaderDict[AddressComb] = 'line['+str(i)+']' 
		elif bool(re.search('.ity+',field,flags=re.I)):
			HeaderDict[City] = 'line['+str(i)+']' 
		elif bool(re.search('.tate',field,flags=re.I)):
			HeaderDict[State] = 'line['+str(i)+']' 
		elif bool(re.match(r'\bzip\b',field,flags=re.I)):
			HeaderDict[Zip] = 'line['+str(i)+']' 
		elif bool(re.search('4z.+',field,flags=re.I)) or\
			bool(re.search('z.+4',field,flags=re.I)):
			HeaderDict[Zip4] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bscf\b',field,flags=re.I)):
			HeaderDict[SCF] = 'line['+str(i)+']' 
		elif bool(re.search('pho.+',field,flags=re.I)):
			HeaderDict[Phone] = 'line['+str(i)+']' 
		elif bool(re.search('HPho.+',field,flags=re.I)) or\
			bool(re.search(r'\bhph\b',field,flags=re.I)):
			HeaderDict[HPhone] = 'line['+str(i)+']' 
		elif bool(re.search('WPho.+',field,flags=re.I)) or\
			bool(re.search(r'\bbph\b',field,flags=re.I)):
			HeaderDict[WPhone] = 'line['+str(i)+']' 
		elif bool(re.search('MPho.+',field,flags=re.I)) or\
			bool(re.search(r'\bcph\b',field,flags=re.I)):
			HeaderDict[MPhone] = 'line['+str(i)+']'
		elif bool(re.search('.mail',field,flags=re.I)):
			HeaderDict[Email] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bvin\b',field,flags=re.I)):
			HeaderDict[VIN] = 'line['+str(i)+']' 
		elif bool(re.search(r'\byear\b',field,flags=re.I)) or\
			bool(re.search(r'\bvyr\b',field,flags=re.I)):
			HeaderDict[Year] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bmake\b',field,flags=re.I)) or\
			bool(re.search(r'\bvmk\b',field,flags=re.I)):
			HeaderDict[Make] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bmodel\b',field,flags=re.I)) or\
			bool(re.search(r'\bvmd\b',field,flags=re.I)):
			HeaderDict[Model] = 'line['+str(i)+']' 
		elif bool(re.search('de.+ate',field,flags=re.I)):
			HeaderDict[DelDate] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bdate\b',field,flags=re.I)):
			HeaderDict[Date] = 'line['+str(i)+']' 
		elif bool(re.search('.adi.+',field,flags=re.I)):
			HeaderDict[Radius] = 'line['+str(i)+']' 
		elif bool(re.search('coor.+',field,flags=re.I)):
			HeaderDict[Coordinates] = 'line['+str(i)+']' 
		elif bool(re.search('v.+len',field,flags=re.I)):
			HeaderDict[VINLen] = 'line['+str(i)+']' 
		elif bool(re.search('dsf.+seq',field,flags=re.I)):
			HeaderDict[DSF_WALK_SEQ] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bcrrt\b',field,flags=re.I)):
			HeaderDict[CRRT] = 'line['+str(i)+']' 
		elif bool(re.search('zip.+rt',field,flags=re.I)):
			HeaderDict[ZipCRRT] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bkbb\b',field,flags=re.I)):
			HeaderDict[KBB] = 'line['+str(i)+']' 
		elif bool(re.search('buy.+val.+',field,flags=re.I)):
			HeaderDict[BuybackValues] = 'line['+str(i)+']' 
		elif bool(re.search('winn.+er',field,flags=re.I)):
			HeaderDict[WinningNum] = 'line['+str(i)+']' 
		elif bool(re.search('mai.+DNQ',field,flags=re.I)):
			HeaderDict[MailDNQ] = 'line['+str(i)+']' 
		elif bool(re.search('bli.+DNQ',field,flags=re.I)):
			HeaderDict[BlitzDNQ] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bdrop\b',field,flags=re.I)):
			HeaderDict[DropVal] = 'line['+str(i)+']'
		elif bool(re.search(r'\bpurl\b',field,flags=re.I)):
			HeaderDict[PURL] = 'line['+str(i)+']'
		elif bool(re.search(r'\bmisc1\b',field,flags=re.I)):
			HeaderDict[Misc1] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bmisc2\b',field,flags=re.I)):
			HeaderDict[Misc2] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bmisc3\b',field,flags=re.I)):
			HeaderDict[Misc3] = 'line['+str(i)+']'
	global i
	global x
	global InputFile
	global OutputFile
	global ReMappedOutputFile
	with open(InputFile,'rU') as InputFile,\
	open(ReMappedOutput,'ab') as ReMappedOutputFile:
		Input = csv.reader(InputFile)
		Output = csv.writer(ReMappedOutputFile)
		Output.writerow(HeaderRow)
		FirstLine = True
		for line in tqdm(Input):
			if CSVFilesHaveHeaderRow and FirstLine:	
				for i in range(0,len(line)):
					match(line[i])
				FirstLine = False
			else:
				newline = []
				for x in range(0,len(HeaderRow)):
					if x in HeaderDict:
						newline.append(eval(HeaderDict[x]))
					else:
						newline.append('')
				Output.writerow(newline)

# Function sets Customer ID Sequence Number
def SetCustomerID():
	if line[DSF_WALK_SEQ] == '':
		line[CustomerID] = 'd' + str(SeqNumDatabase) # Database Record
	elif line[DropVal] == 'p' or line[DropVal] == 'P' or \
	line[DropVal] == 'penny' or line[DropVal] == 'Penny':
		line[CustomerID] = 'p' + str(SeqNumPurchaseP) # Penny
	elif line[DropVal] == 'n' or line[DropVal] == 'N' or \
	line[DropVal] == 'nickel' or line[DropVal] == 'Nickel':
		line[CustomerID] = 'n' + str(SeqNumPurchaseN) # Nickle
	else:
		line[CustomerID] = 'a' + str(SeqNumPurchase) # Purchase Record

# Assign DROP Number
def SetDropIndex():
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

def ZipPlus4Split():
	if len(str(line[Zip])) > 5 and (str(line[Zip]).find('-') == 5):
		FullZip = line[Zip].split('-')
		line[Zip] = FullZip[0]
		line[Zip4] = FullZip[1]
		
# Function Calculates Radius Based on the Central Zip
def CalculateRadiusfromCentralZip():
	if CentralZip in ZipCoordinateDict:
		OriginZipCoord = ZipCoordinateDict[CentralZip]
	else:
		OriginZipCoord = 0
	
	if int(line[Zip][:1]) == 0:
		line[Zip] = line[Zip][-4:]
	
	if line[Zip] in ZipCoordinateDict:
		TargetZipCoord = ZipCoordinateDict[line[Zip]]
		line[Coordinates] = TargetZipCoord
	else:
		TargetZipCoord = 0	
	if OriginZipCoord == 0 or TargetZipCoord == 0:
		line[Radius] = 'n/a'
	else:
		line[Radius] = (float(vincenty(OriginZipCoord,TargetZipCoord).miles))
		
# Select usable phone
def AssignPhone():
	if line[MPhone] != '' and len(line[MPhone]) > 5:
		line[Phone] = line[MPhone]
	elif line[HPhone] != '' and len(line[HPhone]) > 5:
		line[Phone] = line[HPhone]
	elif line[WPhone] != '' and len(line[WPhone]) > 5:
		line[Phone] = line[WPhone]
	else:
		line[Phone] = ''

# Reformat phones 
def ReformatPhones():
	if len(str(line[Phone])) == 10:
		line[Phone] = '(' + str(line[Phone][0:3]) + ') ' +\
		str(line[Phone][3:6]) + '-' + str(line[Phone][6:10])
	elif len(str(line[Phone])) == 7:
		line[Phone] = str(line[Phone][0:3]) + '-' + str(line[Phone][3:7])

# Decodes year column if abreviated year. e.g  2015 = 15 or 2007 = 7
def YearDecode():
	if str(line[Year]) in YearDecodeDict:
		line[Misc1] = YearDecodeDict[line[Year]]
	else:
		line[Misc1] = ''

# Sets Field Case
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

# Deletes VIN# less than 17 characters
def SetVINLen(): 
	line[VINLen] = len(line[VIN])
	if line[VINLen] < 17:
		line[VIN] = ""
	else:
		line[VIN] = str.upper(line[VIN]) 

# Normalize Date Field
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

# Sets Winning# Value
def SetWinningNum(): 
	line[WinningNum] = WinningNumber

# Combines values - Address1 & Address2
def CombineAddress(): 
	if line[AddressComb] == '':
		if line[Address2] == '':
			line[AddressComb] = line[Address1] 
		else:
			line[AddressComb] = line[Address1] + ' ' + line[Address2]
	else:
		line[AddressComb] = str.title(line[AddressComb]) 

# Extrapolate 3-Digit SCF from the ZIP code
def SetSCF(): 
	ZipLen = len(line[Zip])
	if ZipLen < 5:
		line
		line[SCF] = (line[Zip])[:2] 
	else:
		line[SCF] = (line[Zip])[:3]  

# Combined Zip + Crrt Fields
def SetZipCrrt(): 
	if line[Zip] == '' or line[CRRT] == '':
		line[ZipCRRT] = ''
	else:
		if len(line[Zip]) < 5:
			line[ZipCRRT] = '0' + line[Zip] + line[CRRT]
		else:
			line[ZipCRRT] = line[Zip] + line[CRRT]

# Assign 'dnq' to records that dont qualify for mail
def CheckMailDNQ():
	if line[FirstName] == '' or line[LastName] == '':
		line[MailDNQ] = 'dnq'
	else:
		line[MailDNQ] = "" 

# Assign 'dnq' to records that dont qualify for phone blitz
def CheckBlitzDNQ():
	if len(line[Phone]) < 8 or len(line[VIN]) < 17: 
		line[BlitzDNQ] = 'dnq'
	else:
		line[BlitzDNQ] = ""

# Check for Dupes then output
def CheckDupesAndMailQualification(): 
	global CleanOutput
	global Dupes
	global DupesFirstTime
	global CleanOutputFirstTime
	global MDNQFirstTime
	global MDNQ
	# -------------------------------- #
	# CHECK DUPE CRITERIA              #
	# OPHH = One Record Per House Hold #
	# OPP  = One Record Per Person     #
	# VIN  = Vin Number                #
	# -------------------------------- #
	key = (line[AddressComb],line[Zip])
	# key = (line[FirstName],line[LastName],line[AddressComb],line[Zip])
	# key = (line[VIN])
	# -------------------------
	if key not in Entries:
		if line[FirstName] == '' or line[LastName] == '' or \
		int(line[Radius]) >= 50:
			if MDNQFirstTime:
				OutMDNQ = csv.writer(MDNQ)
				OutMDNQ.writerow(HeaderRow)
				OutMDNQ.writerow(line)
				MDNQFirstTime = False
			else:
				OutMDNQ = csv.writer(MDNQ)
				OutMDNQ.writerow(line)
		else:
			if CleanOutputFirstTime:
				OutputClean = csv.writer(CleanOutput)
				OutputClean.writerow(HeaderRow)
				OutputClean.writerow(line)
				Entries.add(key)
				CleanOutputFirstTime = False
			else:
				OutputClean = csv.writer(CleanOutput)
				OutputClean.writerow(line)
				Entries.add(key)
	else:
		if DupesFirstTime:
			OutDupes = csv.writer(Dupes)
			OutDupes.writerow(HeaderRow)
			OutDupes.writerow(line)
			DupesFirstTime = False
		else:
			OutDupes = csv.writer(Dupes)
			OutDupes.writerow(line)

# Output Processed Database, Purchase & Duplicate Files
def SecondaryOutputDatabase():
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
		'Winning Number',\
		'Drop'\
		]
	DatabaseOutputHeader = (\
		line[CustomerID],\
		line[FirstName],\
		line[LastName],\
		line[AddressComb],\
		line[City],\
		line[State],\
		line[Zip],\
		line[Phone],\
		line[Year],\
		line[Make],\
		line[Model],\
		line[WinningNum],\
		line[DropVal]\
		)
	global DatabaseFirstTime
	global CleanOutputDatabase	
	if DatabaseFirstTime:
		CleanOutputDatabase = open(CleanOutputDatabase,'ab')
		OutputCleanDatabase = csv.writer(CleanOutputDatabase)
		OutputCleanDatabase.writerow(HeaderRowDatabase)
		OutputCleanDatabase.writerow(DatabaseOutputHeader)
		DatabaseFirstTime = False
	else:
		OutputCleanDatabase = csv.writer(CleanOutputDatabase)
		OutputCleanDatabase.writerow(DatabaseOutputHeader)

def SecondaryOutputPurchase():
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
		'Crrt',\
		'Winning Number',\
		'Drop'\
		]
	PurchaseOutputHeader = (\
		line[CustomerID],\
		line[FirstName],\
		line[LastName],\
		line[AddressComb],\
		line[City],\
		line[State],\
		line[Zip],\
		line[Zip4],\
		line[DSF_WALK_SEQ],\
		line[CRRT],\
		line[WinningNum],\
		line[DropVal]\
		)
	global PurchaseFirstTimeP
	global PurchaseFirstTimeN
	global PurchaseFirstTime
	global PurchaseFirstTimeAll
	global CleanOutputPurchaseP
	global CleanOutputPurchaseN
	global CleanOutputPurchaseR
	global CleanOutputPurchaseAll

	if PurchaseFirstTimeAll:
		CleanOutputPurchaseAll = open(CleanOutputPurchaseAll,'ab')
		OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
		OutputCleanPurchaseAll.writerow(HeaderRowPurchase)
		OutputCleanPurchaseAll.writerow(PurchaseOutputHeader)
		PurchaseFirstTimeAll = False
	else:
		OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
		OutputCleanPurchaseAll.writerow(PurchaseOutputHeader)

	if line[CustomerID][:1] == 'p' or (line[CustomerID])[:1] == 'P': 
		if PurchaseFirstTimeP:
			CleanOutputPurchaseP = open(CleanOutputPurchaseP,'ab')
			OutputCleanPurchaseP = csv.writer(CleanOutputPurchaseP)
			OutputCleanPurchaseP.writerow(HeaderRowPurchase)
			OutputCleanPurchaseP.writerow(PurchaseOutputHeader)
			PurchaseFirstTimeP = False
		else:
			OutputCleanPurchaseP = csv.writer(CleanOutputPurchaseP)
			OutputCleanPurchaseP.writerow(PurchaseOutputHeader)
	elif line[CustomerID][:1] == 'n' or (line[CustomerID])[:1] == 'N': 
		if PurchaseFirstTimeN:
			CleanOutputPurchaseN = open(CleanOutputPurchaseN,'ab')
			OutputCleanPurchaseN = csv.writer(CleanOutputPurchaseN)
			OutputCleanPurchaseN.writerow(HeaderRowPurchase)
			OutputCleanPurchaseN.writerow(PurchaseOutputHeader)
			PurchaseFirstTimeN = False
		else:
			OutputCleanPurchaseN = csv.writer(CleanOutputPurchaseN)
			OutputCleanPurchaseN.writerow(PurchaseOutputHeader)
	elif line[CustomerID][:1] == 'a' or (line[CustomerID])[:1] == 'A': 
		if PurchaseFirstTime:
			CleanOutputPurchaseR = open(CleanOutputPurchaseR,'ab')
			OutputCleanPurchaseR = csv.writer(CleanOutputPurchaseR)
			OutputCleanPurchaseR.writerow(HeaderRowPurchase)
			OutputCleanPurchaseR.writerow(PurchaseOutputHeader)
			PurchaseFirstTime = False
		else:
			OutputCleanPurchaseR = csv.writer(CleanOutputPurchaseR)
			OutputCleanPurchaseR.writerow(PurchaseOutputHeader)

def GenerateAppendOutput():
	HeaderRowAppend = [\
		'PURL',\
		'First Name',\
		'Last Name',\
		'Address1',\
		'City',\
		'State',\
		'Zip',\
		'4Zip',\
		'Crrt',\
		'DSF_WALK_SEQ',\
		'Customer ID',\
		'Drop'\
		]
	AppendOutputHeader = (\
		line[PURL],\
		line[FirstName],\
		line[LastName],\
		line[Address1],\
		line[City],\
		line[State],\
		line[Zip],\
		line[Zip4],\
		line[CRRT],\
		line[DSF_WALK_SEQ],\
		line[CustomerID],\
		line[DropVal]\
		)
	global AppendFirstTimeP
	global AppendFirstTimeN
	global AppendFirstTime
	global CleanOutputAppendP
	global CleanOutputAppendN
	global CleanOutputAppend

	if line[CustomerID][:1] == 'p' or line[CustomerID][:1] == 'P': 
		if AppendFirstTimeP:
			CleanOutputAppendP = open(CleanOutputAppendP,'ab')
			OutputCleanAppendP = csv.writer(CleanOutputAppendP)
			OutputCleanAppendP.writerow(HeaderRowAppend)
			OutputCleanAppendP.writerow(AppendOutputHeader)
			AppendFirstTimeP = False
		else:
			OutputCleanAppendP = csv.writer(CleanOutputAppendP)
			OutputCleanAppendP.writerow(AppendOutputHeader)
	elif line[CustomerID][:1] == 'n' or line[CustomerID][:1] == 'N': 
		if AppendFirstTimeN:
			CleanOutputAppendN = open(CleanOutputAppendN,'ab')
			OutputCleanAppendN = csv.writer(CleanOutputAppendN)
			OutputCleanAppendN.writerow(HeaderRowAppend)
			OutputCleanAppendN.writerow(AppendOutputHeader)
			AppendFirstTimeN = False
		else:
			OutputCleanAppendN = csv.writer(CleanOutputAppendN)
			OutputCleanAppendN.writerow(AppendOutputHeader)
	elif line[CustomerID][:1] == 'a' or line[CustomerID][:1] == 'A': 
		if AppendFirstTime:
			CleanOutputAppend = open(CleanOutputAppend,'ab')
			OutputCleanAppend = csv.writer(CleanOutputAppend)
			OutputCleanAppend.writerow(HeaderRowAppend)
			OutputCleanAppend.writerow(AppendOutputHeader)
			AppendFirstTime = False
		else:
			OutputCleanAppend = csv.writer(CleanOutputAppend)
			OutputCleanAppend.writerow(AppendOutputHeader)

# Output Phone List File
def ExtractPhonesList():
	HeaderRowPhones = [\
		'First Name',\
		'Last Name',\
		'Phone',\
		'Address',\
		'City',\
		'State',\
		'Zip',\
		'Last Trade Year',\
		'Last Trade Make',\
		'Last Trade Model'\
		]
	HeaderOutputPhones = (\
		line[FirstName],\
		line[LastName],\
		line[Phone],\
		line[AddressComb],\
		line[City],\
		line[State],\
		line[Zip],\
		line[Year],\
		line[Make],\
		line[Model]\
		)
	global PhonesFirstTime
	global CleanOutputPhones
	if line[Phone] != '':
		if PhonesFirstTime:
			CleanOutputPhones = open(CleanOutputPhones,'ab')
			OutputPhones = csv.writer(CleanOutputPhones)
			OutputPhones.writerow(HeaderRowPhones)
			OutputPhones.writerow(HeaderOutputPhones)
			PhonesFirstTime = False
		else:
			OutputPhones = csv.writer(CleanOutputPhones)
			OutputPhones.writerow(HeaderOutputPhones)
# ---------------------------------------------
# Main Program
if HRSelect == 'Y' or HRSelect == 'y':
	Selection = ReMappedOutput
	ReMapHeaderFields()
else:
	Selection = InputFile

with open(Selection,'rU') as InputFile, open(CleanOutput,'ab') as CleanOutput,\
open(Dupes,'ab') as Dupes, open(MDNQ,'ab') as MDNQ:
	Input = csv.reader(InputFile)
	FirstLine = True
	for line in tqdm(Input):
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			SetZipCrrt()
			SetDropIndex()
			if line[PURL] == '':
				SetCustomerID()
			AssignPhone()
			ReformatPhones()
			SetCase()
			CombineAddress()
			ZipPlus4Split()
			CalculateRadiusfromCentralZip()
			YearDecode()
			SetVINLen()
			SetDateFormat()
			SetWinningNum()
			SetSCF()
			CheckMailDNQ()
			CheckBlitzDNQ()
			CheckDupesAndMailQualification()
			if line[DSF_WALK_SEQ] == '':
				SecondaryOutputDatabase()
			else:
				if line[PURL] == '':
					SecondaryOutputPurchase()
				else:
					GenerateAppendOutput()
			ExtractPhonesList()
		if line[DSF_WALK_SEQ] == '':
			SeqNumDatabase+=1
		elif line[DropVal] == 'p' or line[DropVal] == 'P':
			SeqNumPurchaseP+=1
		elif line[DropVal] == 'n' or line[DropVal] == 'N':
			SeqNumPurchaseN+=1
		else:
			SeqNumPurchase+=1
# ---------------------------------------------
if line[DSF_WALK_SEQ] == '':
 	CleanOutputDatabase.close()
elif (line[CustomerID])[:1] == 'p' or (line[CustomerID])[:1] == 'P':
	if line[PURL] == '':
		CleanOutputPurchaseP.close()
	else:
		CleanOutputAppendP.close()
elif (line[CustomerID])[:1] == 'n' or (line[CustomerID])[:1] == 'N':
	if line[PURL] == '':
		CleanOutputPurchaseN.close()
	else:
		CleanOutputAppendN.close()
else:
	if line[PURL] == '':
 		CleanOutputPurchaseR.close()
 	else:
		CleanOutputAppend.close() 	
if line[Phone] != '':
	CleanOutputPhones.close()
# ---------------------------------------------
ProcDataFrame = pd.read_csv(CleanOutputPD, low_memory=False)
DF = ProcDataFrame.loc[:,['Radius']]
print(DF.describe())
# ---------------------------------------------

