#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, re, glob
import pandas as pd
from geopy.distance import vincenty
from dateutil.parser import *
from datetime import *
from tqdm import tqdm
from nameparser import HumanName
# ---------------------------------------------
os.chdir('../../../../Desktop/')
path = '../Dropbox/HUB/Projects/_Resources'

MDNQFile = os.path.join(path,'MDNQ.csv')
DropFile = os.path.join(path,'Drop_File.csv')
ZipCoordFile = os.path.join(path,'US_ZIP_Coordinates.csv')
YearDecodeFile = os.path.join(path,'Year_Decode.csv')
GenSuppressionFile = os.path.join(path,'GEN_Suppression.csv')
MonthlySuppressionFile = os.path.join(path,'Monthly_Suppression.csv')
# ---------------------------------------------
SeqNumDatabase = 10000
SeqNumPurchaseP = 30000
SeqNumPurchaseN = 40000
SeqNumPurchase = 50000

PennyCounter = 0
NickelCounter = 0
DatabaseCounter = 0
PurchaseCounter = 0
MDNQCounter = 0
DupesCounter = 0

Entries = set()
DoNotMailFile = set()
# ---------------------------------------------
# Import Zip Dictionary from US_ZIP_Coordinates.csv file
try:
	ZipCoordinateDict = {}
	with open(ZipCoordFile,'rU') as ZipCoordFile:
		ZipCoordinate = csv.reader(ZipCoordFile)
		FirstLine = True
		for line in ZipCoordinate:
			if FirstLine:
				FirstLine = False
			else:
				ZipCoordinateDict[line[0]] = (line[1], line[2])
except:
	print('Zip Dictionary File not located')
# ---------------------------------------------
# Import GENERAL Suppression File for the purposes of de-duping
try:
	with open(GenSuppressionFile,'rU') as GenSuppressionFile:
		GenSuppression = csv.reader(GenSuppressionFile)
		FirstLine = True
		for line in GenSuppression:
			if FirstLine:
				FirstLine = False
			else:
				Entries.add((str.title(line[2]),str.title(line[5])))
except:
	print('GENERAL Suppression File not loaded')
# ---------------------------------------------
# Import Montly Suppression File for the purposes of de-duping
try:
	with open(MonthlySuppressionFile,'rU') as MonthlySuppressionFile:
		MonthlySuppression = csv.reader(MonthlySuppressionFile)
		FirstLine = True
		for line in MonthlySuppression:
			if FirstLine:
				FirstLine = False
			else:
				Entries.add((str.title(line[2]),str.title(line[5])))
except:
	print('Montly Suppression File not loaded')
# ---------------------------------------------
# Import Mail DNQ File for the purposes of de-duping
try:
	with open(MDNQFile,'rU') as MDNQFile:
		MDNQ = csv.reader(MDNQFile)
		FirstLine = True
		for line in MDNQ:
			if FirstLine:
				FirstLine = False
			else:
				DoNotMailFile.add(line[0])
except:
	print('Mail DNQ File not loaded')
# ---------------------------------------------
# Import Drop Dictionary from Drop_File.csv file
try:
	DropDict = {}
	with open(DropFile,'rU') as DropFile:
		Drop = csv.reader(DropFile)
		FirstLine = True
		for line in Drop:
			if FirstLine:
				FirstLine = False
			else:
				DropDict[line[0]] = line[1]
except:
	print('Drop Dictionary File not loaded')
# ---------------------------------------------
# Import Year Decode Dictionary from Year_Decode.csv file
try:
	YearDecodeDict = {}
	with open(YearDecodeFile,'rU') as YearDecodeFile:
		YearDecode = csv.reader(YearDecodeFile)
		FirstLine = True
		for line in YearDecode:
			if FirstLine:
				FirstLine = False
			else:
				YearDecodeDict[line[0]] = (line[1])
except:
	print('Year Decode Dictionary File not loaded')
# ---------------------------------------------
IPFName = raw_input('File Name................ : ')
InputFile = IPFName + '.csv'
CentralZip = raw_input('Enter Central ZIP codes.. : ')
while CentralZip not in ZipCoordinateDict:
	CentralZip = raw_input('Enter Valid Central ZIP Codes : ')
MaxRadius = int(raw_input('Enter Maximum Radius..... : '))
# ---------------------------------------------
# Import LOCAL Suppression File for the purposes of de-duping
try:
	SuppressionFileName = raw_input('Enter Suppression Name... : ')
	SuppressionFile = SuppressionFileName+'.csv'
	if SuppressionFileName != '':
		with open(SuppressionFile,'rU') as SuppressionFile:
			Suppression = csv.reader(SuppressionFile)
			FirstLine = True
			for line in Suppression:
				if FirstLine:
					FirstLine = False
				else:
					Entries.add((str.title(line[2]),str.title(line[5])))
except:
	print('Local suppression file not loaded')
# ---------------------------------------------
ReMappedOutput = '>>> ' + IPFName + '_Re-Mapped.csv'
Dupes = '>>> DUPES.csv'
MDNQ = '>>> M-DNQ.csv'
CleanOutput = IPFName + ' OutputMAIN.csv'
CleanOutputPD = IPFName + ' OutputMAIN.csv'
AppendMonthlySuppFile = IPFName + ' Add Monthly Suppression List.csv'
CleanOutputPhones = IPFName + ' PHONES List.csv'
CleanOutputDatabase = IPFName + ' UPLOAD DATA List.csv'
CleanOutputPurchaseAll = IPFName + ' UPLOAD List.csv'
CleanOutputAppendP = IPFName + ' PENNY List.csv'
CleanOutputAppendN = IPFName + ' NICKEL List.csv'
CleanOutputAppendR = IPFName + ' OTHER List.csv'
# ---------------------------------------------
# Assign Variables For Readability
CustomerID = 0
FullName = 1
FirstName = 2
MI = 3
LastName = 4
Address1 = 5
Address2 = 6
AddressComb = 7
City = 8
State = 9
Zip = 10
Zip4 = 11
SCF = 12
Phone = 13
HPhone = 14
WPhone = 15
MPhone = 16
Email = 17
VIN = 18
Year = 19
Make = 20
Model = 21
DelDate = 22
Date = 23
Radius = 24
Coordinates = 25
VINLen = 26
DSF_WALK_SEQ = 27
CRRT = 28
ZipCRRT = 29
KBB = 30
BuybackValues = 31
WinningNum = 32
MailDNQ = 33
BlitzDNQ = 34
DropVal = 35
PURL = 36
YrDec = 37
Misc1 = 38
Misc2 = 39
Misc3 = 40

# Assign Column Names To Header Output Files
HeaderRow = [\
	'Customer ID',\
	'FullName',\
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
	'YrDec',\
	'Misc1',\
	'Misc2',\
	'Misc3'\
	]
# ------------------------------------------- #
# M a i n - P r o g r a m                     #
# ------------------------------------------- #
HRSelect = 'Y'
if HRSelect == 'Y' or HRSelect == 'y':
	Selection = ReMappedOutput
	# Re-Map Header Fields
	HeaderDict = {}
	def match(field):
		if bool(re.search('cus.+id',field,flags=re.I)):
			HeaderDict[CustomerID] = 'line['+str(i)+']'
		elif bool(re.search('ful.+me',field,flags=re.I)):
			HeaderDict[FullName] = 'line['+str(i)+']'
		elif bool(re.search('fir.+me',field,flags=re.I)):
			HeaderDict[FirstName] = 'line['+str(i)+']'
		elif bool(re.search(r'\bmi\b',field,flags=re.I)) or \
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
		elif bool(re.search('4z.+',field,flags=re.I)) or \
		bool(re.search('z.+4',field,flags=re.I)):
			HeaderDict[Zip4] = 'line['+str(i)+']'
		elif bool(re.search(r'\bscf\b',field,flags=re.I)):
			HeaderDict[SCF] = 'line['+str(i)+']'
		elif bool(re.search('pho.+',field,flags=re.I)):
			HeaderDict[Phone] = 'line['+str(i)+']'
		elif bool(re.search('HPho.+',field,flags=re.I)) or \
		bool(re.search(r'\bhph\b',field,flags=re.I)):
			HeaderDict[HPhone] = 'line['+str(i)+']'
		elif bool(re.search('WPho.+',field,flags=re.I)) or \
		bool(re.search(r'\bbph\b',field,flags=re.I)):
			HeaderDict[WPhone] = 'line['+str(i)+']'
		elif bool(re.search('MPho.+',field,flags=re.I)) or \
		bool(re.search(r'\bcph\b',field,flags=re.I)):
			HeaderDict[MPhone] = 'line['+str(i)+']'
		elif bool(re.search('.mail',field,flags=re.I)):
			HeaderDict[Email] = 'line['+str(i)+']'
		elif bool(re.search(r'\bvin\b',field,flags=re.I)):
			HeaderDict[VIN] = 'line['+str(i)+']'
		elif bool(re.search(r'\byear\b',field,flags=re.I)) or \
		bool(re.search(r'\bvyr\b',field,flags=re.I)):
			HeaderDict[Year] = 'line['+str(i)+']'
		elif bool(re.search(r'\bmake\b',field,flags=re.I)) or \
		bool(re.search(r'\bvmk\b',field,flags=re.I)):
			HeaderDict[Make] = 'line['+str(i)+']'
		elif bool(re.search(r'\bmodel\b',field,flags=re.I)) or \
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
		elif bool(re.search(r'\byrdec\b',field,flags=re.I)):
			HeaderDict[YrDec] = 'line['+str(i)+']'
		elif bool(re.search(r'\bmisc1\b',field,flags=re.I)):
			HeaderDict[Misc1] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bmisc2\b',field,flags=re.I)):
			HeaderDict[Misc2] = 'line['+str(i)+']' 
		elif bool(re.search(r'\bmisc3\b',field,flags=re.I)):
			HeaderDict[Misc3] = 'line['+str(i)+']'
	
	with open(InputFile,'rU') as InputFile, \
	open(ReMappedOutput,'ab') as ReMappedOutputFile:
		Input = csv.reader(InputFile)
		Output = csv.writer(ReMappedOutputFile)
		Output.writerow(HeaderRow)
		FirstLine = True
		for line in tqdm(Input):
			if FirstLine:	
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
else:
	Selection = InputFile
# ---------------------------------------------
with open(Selection,'rU') as InputFile, \
open(CleanOutput,'ab') as CleanOutput, \
open(Dupes,'ab') as Dupes, \
open(MDNQ,'ab') as MDNQ, \
open(CleanOutputPhones,'ab') as CleanOutputPhones, \
open(CleanOutputDatabase,'ab') as CleanOutputDatabase, \
open(CleanOutputPurchaseAll,'ab') as CleanOutputPurchaseAll, \
open(CleanOutputAppendP,'ab') as CleanOutputAppendP, \
open(CleanOutputAppendN,'ab') as CleanOutputAppendN, \
open(CleanOutputAppendR,'ab') as CleanOutputAppendR, \
open(AppendMonthlySuppFile,'ab') as AppendMonthlySupp:
	
	CleanOutputFirstTime = True
	DatabaseFirstTime = True
	PurchaseFirstTimeP = True
	PurchaseFirstTimeN = True
	PurchaseFirstTimeR = True
	PurchaseFirstTimeAll = True
	PhonesFirstTime = True
	DupesFirstTime = True
	AppendFirstTimeP = True
	AppendFirstTimeN = True
	AppendFirstTimeR = True
	MDNQFirstTime = True
	MonthlySuppressionFirstTime = True

	Input = csv.reader(InputFile)
	FirstLine = True
	for line in tqdm(Input):
		if FirstLine:
			FirstLine = False
		else:
			# ---------------------------------------------
			# Parse fullname field if required
			if line[FullName] != '' and line[FirstName] == '' \
			and line[LastName] == '':
				ParsedFName = HumanName(str.title(line[FullName]))
				line[FirstName] = ParsedFName.first.encode('utf-8')
				line[MI] = ParsedFName.middle.encode('utf-8')
				line[LastName] = ParsedFName.last.encode('utf-8')
			# ---------------------------------------------
			# Split ZIP code to ZIP + ZIP4 components if required
			if len(str(line[Zip])) > 5 and (str(line[Zip]).find('-') == 5):
				FullZip = line[Zip].split('-')
				line[Zip] = FullZip[0]
				line[Zip4] = FullZip[1]
			# ---------------------------------------------
			# Combine ZIP+CRRT
			if line[Zip] == '' or line[CRRT] == '':
				line[ZipCRRT] = ''
			elif len(str(line[Zip])) < 5:
				line[ZipCRRT] = '0' + line[Zip] + line[CRRT]
			else:
				line[ZipCRRT] = line[Zip] + line[CRRT]
			# ---------------------------------------------
			# Combine Address1 & Address2
			if line[AddressComb] == '' and line[Address1] != '' and \
			line[Address2] != '':
				line[AddressComb] = str.title(line[Address1]) + ' ' \
				+ str.title(line[Address2])
			elif line[Address1] != '' and line[Address2] == '':
				line[AddressComb] = str.title(line[Address1]) 
			else:
				line[AddressComb] = str.title(line[AddressComb])
			# ---------------------------------------------
			# Set Drop Index from Drop Dictionary and Set Customer ID
			if line[PURL] == '':
				if line[ZipCRRT] in DropDict:
					line[DropVal] = DropDict[line[ZipCRRT]]
					if line[DropVal] == 'p' or line[DropVal] == 'P' or \
					line[DropVal] == 'penny' or line[DropVal] == 'Penny':
						line[CustomerID] = 'p' + str(SeqNumPurchaseP)
						SeqNumPurchaseP += 1
						PennyCounter += 1
					elif line[DropVal] == 'n' or line[DropVal] == 'N' or \
					line[DropVal] == 'nickel' or line[DropVal] == 'Nickel':
						line[CustomerID] = 'n' + str(SeqNumPurchaseN)
						SeqNumPurchaseN += 1
						NickelCounter += 1
				elif line[DSF_WALK_SEQ] == '':
					line[DropVal] = 'd'
					line[CustomerID] = 'd' + str(SeqNumDatabase)
					SeqNumDatabase += 1
					DatabaseCounter += 1
				elif line[DSF_WALK_SEQ] != '':
					line[DropVal] = 'a'
					line[CustomerID] = 'a' + str(SeqNumPurchase)
					SeqNumPurchase += 1
					PurchaseCounter += 1
			else:
				if line[DropVal] == 'p' or line[DropVal] == 'P' or \
				line[DropVal] == 'Penny' or line[DropVal] == 'penny':
					PennyCounter += 1
				elif line[DropVal] == 'n' or line[DropVal] == 'N' or \
				line[DropVal] == 'Nickel' or line[DropVal] == 'nickel':
					NickelCounter += 1
				elif line[DropVal] == 'd':
					DatabaseCounter += 1
				elif line[DropVal] == 'a':
					PurchaseCounter += 1	
			# ---------------------------------------------
			# Set Phone # And Reformat
			if line[MPhone] != '' and len(str(line[MPhone])) > 6:
				vp = str(line[MPhone]).strip()
				vp = str(vp).replace('-','')
				vp = str(vp).replace('(','')
				vp = str(vp).replace(')','')
				line[Phone] = str(vp).replace(' ','')
			elif line[HPhone] != '' and len(str(line[HPhone])) > 6:
				vp = str(line[HPhone]).strip()
				vp = str(vp).replace('-','')
				vp = str(vp).replace('(','')
				vp = str(vp).replace(')','')
				line[Phone] = str(vp).replace(' ','')
			elif line[WPhone] != '' and len(str(line[WPhone])) > 6:
				vp = str(line[WPhone]).strip()
				vp = str(vp).replace('-','')
				vp = str(vp).replace('(','')
				vp = str(vp).replace(')','')
				line[Phone] = str(vp).replace(' ','')
			else:
				line[Phone] = ''
			if len(str(line[Phone])) == 10:
				line[Phone] = '(' + str(line[Phone][0:3]) + ') ' + \
				str(line[Phone][3:6]) + '-' + str(line[Phone][6:10])
			elif len(str(line[Phone])) == 7:
				line[Phone] = str(line[Phone][0:3]) + '-' + \
				str(line[Phone][3:7])
			else:
				line[Phone] = ''
			# ---------------------------------------------
			# Set Case for data fields
			line[FullName] = str.title(line[FullName])
			line[FirstName] = str.title(line[FirstName])
			if len(str(line[MI])) == 1:
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
			# ---------------------------------------------
			# Year Decode
			if str(line[Year]) in YearDecodeDict:
				line[YrDec] = YearDecodeDict[line[Year]]
			else:
				line[YrDec] = ''
			# ---------------------------------------------
			# Set VIN Length
			line[VINLen] = len(str(line[VIN]))
			if line[VINLen] < 17:
				line[VIN] = ''
			else:
				line[VIN] = str.upper(line[VIN])
			# ---------------------------------------------
			# Set Date Format
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
			# ---------------------------------------------
			# Set Winning Number
			line[WinningNum] = 40754
			# ---------------------------------------------
			# Set SCF
			ZipLen = len(str(line[Zip]))
			if ZipLen < 5:
				line[SCF] = (line[Zip])[:2]
			else:
				line[SCF] = (line[Zip])[:3]
			# ---------------------------------------------
			# Check Blitz DNQ
			if len(str(line[Phone])) < 8 or len(str(line[VIN])) < 17:
				line[BlitzDNQ] = 'dnq'
			else:
				line[BlitzDNQ] = ''
			# ---------------------------------------------
			# Calculate Radius from Central Zip
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
				line[Radius] = '9999'
			else:
				line[Radius] = float(vincenty(OriginZipCoord,TargetZipCoord).miles)
			# --------------------------------------------- 
			# Extract Phone List
			if line[Phone] != '' and line[FirstName] != '' and \
			line[LastName] != '' and line[BlitzDNQ] != 'dnq':
				HeaderRowPhones = [\
					'First Name',\
					'Last Name',\
					'Phone',\
					'Address',\
					'City',\
					'State',\
					'Zip',\
					'Last Veh Year',\
					'Last Veh Make',\
					'Last Veh Model'\
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
				if PhonesFirstTime:
					OutputPhones = csv.writer(CleanOutputPhones)
					OutputPhones.writerow(HeaderRowPhones)
					OutputPhones.writerow(HeaderOutputPhones)
					PhonesFirstTime = False
				else:
					OutputPhones = csv.writer(CleanOutputPhones)
					OutputPhones.writerow(HeaderOutputPhones)
			# --------------------------------------------- #
			# Check for Dupes and Mail Qualification
			key = (line[AddressComb],line[Zip])
			# key = (line[FirstName],line[LastName],line[AddressComb],line[Zip])
			# key = (line[VIN])
			if key not in Entries:
				if line[FirstName] == '' or line[LastName] == '' or \
				str.lower(line[FirstName]) in DoNotMailFile or \
				str.lower(line[MI]) in DoNotMailFile or \
				str.lower(line[LastName]) in DoNotMailFile or \
				float(line[Radius]) > MaxRadius:
					if MDNQFirstTime:
						OutMDNQ = csv.writer(MDNQ)
						OutMDNQ.writerow(HeaderRow)
						OutMDNQ.writerow(line)
						MDNQFirstTime = False
						MDNQCounter += 1
					else:
						OutMDNQ = csv.writer(MDNQ)
						OutMDNQ.writerow(line)
						MDNQCounter += 1
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
					DupesCounter += 1
				else:
					OutDupes = csv.writer(Dupes)
					OutDupes.writerow(line)
					DupesCounter += 1
			# --------------------------------------------- #
			if line[PURL] != '':
				# Generate Monthly Suppression File
				HeaderRow = [\
					'First Name',\
					'Last Name',\
					'Address',\
					'City',\
					'State',\
					'Zip',\
					'Campaign Name'\
					]
				HeaderRowOutput = (\
					line[FirstName],\
					line[LastName],\
					line[AddressComb],\
					line[City],\
					line[State],\
					line[Zip],\
					IPFName
					)
				if MonthlySuppressionFirstTime:
					MonthlySupp = csv.writer(AppendMonthlySupp)
					MonthlySupp.writerow(HeaderRow)
					MonthlySupp.writerow(HeaderRowOutput)
					MonthlySuppressionFirstTime = False
				else:
					MonthlySupp = csv.writer(AppendMonthlySupp)
					MonthlySupp.writerow(HeaderRowOutput)
			# --------------------------------------------- #
			if line[DSF_WALK_SEQ] == '' and line[PURL] == '':
				# Genrate Secondary Output Database File
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
					'Position'\
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
				if DatabaseFirstTime:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(HeaderRowDatabase)
					OutputCleanDatabase.writerow(DatabaseOutputHeader)
					DatabaseFirstTime = False
				else:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(DatabaseOutputHeader)

			elif line[DSF_WALK_SEQ] != '' and line[PURL] == '':
				# Generate Secondary Output Purchase
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
					'Position'\
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
				if PurchaseFirstTimeAll:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchase)
					OutputCleanPurchaseAll.writerow(PurchaseOutputHeader)
					PurchaseFirstTimeAll = False
				else:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(PurchaseOutputHeader)

			else:
				# Generate Append Output File
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
					'Position'\
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
				if line[CustomerID][:1] == 'p' or line[CustomerID][:1] == 'P':
					if AppendFirstTimeP:
						OutputCleanAppendP = csv.writer(CleanOutputAppendP)
						OutputCleanAppendP.writerow(HeaderRowAppend)
						OutputCleanAppendP.writerow(AppendOutputHeader)
						AppendFirstTimeP = False
					else:
						OutputCleanAppendP = csv.writer(CleanOutputAppendP)
						OutputCleanAppendP.writerow(AppendOutputHeader)
				elif line[CustomerID][:1] == 'n' or line[CustomerID][:1] == 'N':
					if AppendFirstTimeN:
						OutputCleanAppendN = csv.writer(CleanOutputAppendN)
						OutputCleanAppendN.writerow(HeaderRowAppend)
						OutputCleanAppendN.writerow(AppendOutputHeader)
						AppendFirstTimeN = False
					else:
						OutputCleanAppendN = csv.writer(CleanOutputAppendN)
						OutputCleanAppendN.writerow(AppendOutputHeader)
				else: 
					if AppendFirstTimeR:
						OutputCleanAppendR = csv.writer(CleanOutputAppendR)
						OutputCleanAppendR.writerow(HeaderRowAppend)
						OutputCleanAppendR.writerow(AppendOutputHeader)
						AppendFirstTimeR = False
					else:
						OutputCleanAppendR = csv.writer(CleanOutputAppendR)
						OutputCleanAppendR.writerow(AppendOutputHeader)

# ---------------------------------------------
# Upkeep - Remove temporary files
Files = glob.glob('*.csv')
for record in Files:
	if os.path.getsize(record) == 0:
		os.remove(record)
	if bool(re.match('.+Re-Mapped.+',record,flags=re.I)):
		os.remove(record)
# ---------------------------------------------
# Terminal Output
try:
	ProcDataFrame = pd.read_csv(CleanOutputPD, low_memory = False)
	ProcDataF = ProcDataFrame.loc[:,['Radius','Year','DelDate']]
	print('===================================')
	print(ProcDataF.describe())
	print('===================================')
	print('   DATABASE Count = {}'.format(DatabaseCounter))
	print('   PURCHASE Count = {}'.format(PurchaseCounter))
	print('      PENNY Count = {}'.format(PennyCounter))
	print('     NICKEL Count = {}'.format(NickelCounter))
	print('  Less MDNQ Count = ({})'.format(MDNQCounter))
	print(' Less Dupes Count = ({})'.format(DupesCounter))
	print('==== T O T A L ==== {}'.format(DatabaseCounter + PurchaseCounter + \
		PennyCounter + NickelCounter - MDNQCounter - DupesCounter))
except:
	print('Empty File')
