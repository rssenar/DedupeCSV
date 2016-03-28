#!/usr/bin/env python
# ==================================================================== #
from __future__ import division, print_function
import csv, os, sys, re, glob
import datetime
from dateutil.parser import *
from geopy.distance import vincenty
from nameparser import HumanName
from tqdm import tqdm
# ==================================================================== #
def main():
	global IPFName
	global PennyCounter
	global NickelCounter
	global DatabaseCounter
	global PurchaseCounter
	global MDNQCounter
	global DupesCounter
	global YearDictCounter
	global MakeDictCounter
	global SCFDictCounter
	global RadiusDictCounter
	global CityDictCounter
	global StateDictCounter
	global SCF3DFacilityCounter
	global ZipCounter
	global IPFName
	global CentralZip
	global MaxRadius
	global MaxYear
	global MinYear
	global CurrentDateUpdate
	global MaxSaleYear
	global CentralZipSCFFacilityReport
	# ==================================================================== #
	os.chdir('../../../../Desktop/') # Change PWD to Desktop
	# ==================================================================== #
	path = '../Dropbox/HUB/Projects/PremWorks/_Resources' # Set path to resource folder
	MDNQFile = os.path.join(path,'MailDNQ.csv')
	DropFile = os.path.join(path,'_DropFile.csv')
	ZipCoordFile = os.path.join(path,'USZIPCoordinates.csv')
	YearDecodeFile = os.path.join(path,'YearDecode.csv')
	GenSuppressionFile = os.path.join(path,'_GeneralSuppression.csv')
	MonthlySuppressionFile = os.path.join(path,'_MonthlySuppression.csv')
	SCF3DigitFile = os.path.join(path,'SCFFacilites.csv')
	# ==================================================================== #
	# Set Initial Variables
	WinninNumber = 40754
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
	SCF3DigitFacility = 0
	Entries = set()
	DoNotMailFile = set()
	# ==================================================================== #
	# Initialize Functions
	# ==================================================================== #
	def SplitAndStripFunc(input):
		AppendedList = []
		input = input.split("|")
		for item in input:
			item = item.strip()
			item = str.title(item)
			AppendedList.append(item)
		return AppendedList
	# ==================================================================== #
	# Initialize Dictionaries
	# ==================================================================== #
	# Import Drop Dictionary from Drop_File.csv file
	try:
		DropDict = {}
		with open(DropFile,'rU') as DropFile:
			Drop = csv.reader(DropFile)
			next(DropFile)
			for line in Drop:
				DropDict[line[0]] = line[1]
	except:
		print('ERROR: Unable to Load Drop Dictionary File')
	# ==================================================================== #
	# Import GENERAL Suppression File for the purposes of de-duping
	try:
		with open(GenSuppressionFile,'rU') as GenSuppressionFile:
			GenSuppression = csv.reader(GenSuppressionFile)
			next(GenSuppressionFile)
			for line in GenSuppression:
				Entries.add((str.title(line[2]),str.title(line[5])))
	except:
		print('ERROR: Unable to Load GENERAL Suppression File')
	# ==================================================================== #
	# Import Montly Suppression File for the purposes of de-duping
	try:
		with open(MonthlySuppressionFile,'rU') as MonthlySuppressionFile:
			MonthlySuppression = csv.reader(MonthlySuppressionFile)
			next(MonthlySuppressionFile)
			for line in MonthlySuppression:
				Entries.add((str.title(line[2]),str.title(line[5])))
	except:
		print('ERROR: Unable to Load Montly Suppression File')
	# ==================================================================== #
	# Import Zip Dictionary from US_ZIP_Coordinates.csv file
	try:
		ZipCoordinateDict = {}
		with open(ZipCoordFile,'rU') as ZipCoord:
			ZipCoordinate = csv.reader(ZipCoord)
			for line in ZipCoordinate:
				ZipCoordinateDict[line[0]] = (line[1], line[2])
	except:
		print('ERROR: Unable to Load Zip Dictionary File')
	# ==================================================================== #
	# Import Mail DNQ File for the purposes of de-duping
	try:
		with open(MDNQFile,'rU') as MDNQFile:
			MDNQ = csv.reader(MDNQFile)
			for line in MDNQ:
				DoNotMailFile.add(str.title(line[0]))
	except:
		print('ERROR: Unable to Load Mail DNQ File')
	# ==================================================================== #
	# Import Year Decode Dictionary from Year_Decode.csv file
	try:
		YearDecodeDict = {}
		with open(YearDecodeFile,'rU') as YearDecodeFile:
			YearDecode = csv.reader(YearDecodeFile)
			for line in YearDecode:
				YearDecodeDict[line[0]] = (line[1])
	except:
		print('ERROR: Unable to Load Year Decode Dictionary File')
	# ==================================================================== #
	# Import SCF Dictionary from SCF Facilities.csv file
	try:
		SCF3DigitDict = {}
		with open(SCF3DigitFile,'rU') as SCF3DigitFile:
			SCF3Digit = csv.reader(SCF3DigitFile)
			for line in SCF3Digit:
				SCF3DigitDict[line[0]] = (line[1])
	except:
		print('ERROR: Unable to Load SCF 3-Digit Dictionary File')
	# ==================================================================== #
	# User Input
	# ==================================================================== #
	# Capture Input - File Name
	IPFName = raw_input('Enter File Name ..................... : ')
	InputFile = IPFName + '.csv'
	while os.path.isfile(InputFile) == False:
		IPFName = raw_input('ERROR: Enter File Name .............. : ')
		InputFile = IPFName + '.csv'
	# Capture Input - Central Zip
	CentralZip = raw_input('Enter Central ZIP Code .............. : ')
	while CentralZip not in ZipCoordinateDict:
		CentralZip = raw_input('ERROR: Enter ZIP Codes............... : ')
	# Capture Input - Max RADIUS
	try:
		MaxRadius = int(raw_input('Enter Max Radius ...............[100] : '))
	except:
		MaxRadius = 100
	# Capture Input - Max YEAR
	try:
		MaxYear = int(raw_input('Enter Max Year ................[2015] : '))
	except:
		MaxYear = 2015
	# Capture Input - Min YEAR
	try:
		MinYear = int(raw_input('Enter Min Year ................[1990] : '))
	except:
		MinYear = 1990
	# Capture Input - Max SALE YEAR
	try:
		MaxSaleYear = int(raw_input('Enter Maximum Sales Year ......[2016] : '))
	except:
		MaxSaleYear = 2016
	# Generate Suppress STATE List
	STATEList = raw_input('Enter Suppression List .......[STATE] : ')
	if STATEList != '':
		STATEList = sorted(SplitAndStripFunc(STATEList))
		print('..STATEList :', STATEList)
	else:
		STATEList = []
		print('..STATEList :', STATEList)
	# Generate Suppress SCF List
	SCFList = raw_input('Enter Suppression List .........[SCF] : ')
	if SCFList != '':
		SCFList = sorted(SplitAndStripFunc(SCFList))
		print('....SCFList :', SCFList)
	else:
		SCFList = []
		print('....SCFList :', SCFList)
	# Generate Suppress YEAR List
	YEARList = raw_input('Enter Suppression List ........[YEAR] : ')
	if YEARList != '':
		YEARList = sorted(SplitAndStripFunc(YEARList))
		print('...YEARList :', YEARList)
	else:
		YEARList = []
		print('...YEARList :', YEARList)
	# Generate Suppress CITY List
	CITYList = raw_input('Enter Suppression List ........[CITY] : ')
	if CITYList != '':
		CITYList = sorted(SplitAndStripFunc(CITYList))
		print('...CITYList :', CITYList)
	else:
		CITYList =[]
		print('...CITYList :', CITYList)
	# Import LOCAL Suppression File for the purposes of de-duping
	SuppressionFileName = raw_input('Enter Suppression File ....[OPTIONAL] : ')
	SuppressionFile = SuppressionFileName + '.csv'
	if SuppressionFileName != '':
		try:
			with open(SuppressionFile,'rU') as SuppressionFile:
				Suppression = csv.reader(SuppressionFile)
				next(SuppressionFile)
				for line in Suppression:
					Entries.add((str.title(line[2]),str.title(line[5])))
		except:
			print('     ERROR: Cannot load local suppression file')
	else:
		print('No Suppression File Selected')
	# Capture ReMap Header Row Selection
	HRSelect = str.upper(raw_input('......ReMap Header Row? [Default = N] : '))
	if HRSelect == '':
		HRSelect = 'N'
	# ==================================================================== #
	ReMappedOutput = '>>>>>>>>>> Re-Mapped <<<<<<<<<<.csv'
	Dupes = '>>>>>>>>>> DUPES <<<<<<<<<<.csv'
	MDNQ = '>>>>>>>>>> M-DNQ <<<<<<<<<<.csv'
	CleanOutput = IPFName + '_UpdatedOutputMain.csv'
	AppendMonthlySuppFile = IPFName + ' Add Monthly Suppression List.csv'
	CleanOutputPhones = IPFName + ' PHONES List.csv'
	CleanOutputDatabase = IPFName + ' UPLOAD DATA List.csv'
	CleanOutputPurchaseAll = IPFName + ' UPLOAD List.csv'
	CleanOutputAppendP = IPFName + ' PENNY List.csv'
	CleanOutputAppendN = IPFName + ' NICKEL List.csv'
	CleanOutputAppendR = IPFName + ' OTHER List.csv'
	# ==================================================================== #
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
	Drop = 35
	PURL = 36
	YrDec = 37
	SCF3DFacility = 38
	Misc1 = 39
	Misc2 = 40
	Misc3 = 41
	# Assign Column Names To Header Output Files
	HeaderRowMain = [\
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
		'SCF3DFacility',\
		'Misc1',\
		'Misc2',\
		'Misc3'\
		]
	# ==================================================================== #
	# ReMap Header
	if HRSelect == 'Y':
		Selection = ReMappedOutput
		HeaderDict = {}
		def match(field): # Match Field Names using Regular Expression
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
				HeaderDict[Drop] = 'line['+str(i)+']'
			elif bool(re.search(r'\bpurl\b',field,flags=re.I)):
				HeaderDict[PURL] = 'line['+str(i)+']'
			elif bool(re.search(r'\byrdec\b',field,flags=re.I)):
				HeaderDict[YrDec] = 'line['+str(i)+']'		
			elif bool(re.search(r'\bSCF3DFacility\b',field,flags=re.I)):
				HeaderDict[SCF3DFacility] = 'line['+str(i)+']'
			elif bool(re.search(r'\bmisc1\b',field,flags=re.I)):
				HeaderDict[Misc1] = 'line['+str(i)+']' 
			elif bool(re.search(r'\bmisc2\b',field,flags=re.I)):
				HeaderDict[Misc2] = 'line['+str(i)+']' 
			elif bool(re.search(r'\bmisc3\b',field,flags=re.I)):
				HeaderDict[Misc3] = 'line['+str(i)+']'
		# Re-Order Fields based on Header Row
		with open(InputFile,'rU') as InputFile, \
		open(ReMappedOutput,'ab') as ReMappedOutputFile:
			Input = csv.reader(InputFile)
			Output = csv.writer(ReMappedOutputFile)
			Output.writerow(HeaderRowMain)
			FirstLine = True
			for line in tqdm(Input):
				if FirstLine:	
					for i in range(0,len(line)):
						match(line[i])
					FirstLine = False
				else:
					newline = []
					for x in range(0,len(HeaderRowMain)):
						if x in HeaderDict:
							newline.append(eval(HeaderDict[x]))
						else:
							newline.append('')
					Output.writerow(newline)
	else:
		Selection = InputFile
	# ==================================================================== #
	# MAIN Function
	# ==================================================================== #
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
		# ============================================================ #
		YearDictCounter = {}
		MakeDictCounter = {}
		ModelDictCounter = {}
		SCFDictCounter = {}
		RadiusDictCounter = {}
		CityDictCounter = {}
		StateDictCounter = {}
		SCF3DFacilityCounter = {}
		ZipCounter = {}
		# ============================================================ #
		Input = csv.reader(InputFile)
		next(InputFile) # Skip Header Row
		for line in tqdm(Input):
			# ============================================================ #
			line[WinningNum] = WinninNumber
			# Parse Fullname if First & Last Name fields are missing
			if line[FullName] != '' and (line[FirstName] == '' \
			and line[LastName] == ''):
				try:
					ParsedFName = HumanName(str.title(line[FullName]))
					line[FirstName] = ParsedFName.first.encode('utf-8')
					line[MI] = ParsedFName.middle.encode('utf-8')
					line[LastName] = ParsedFName.last.encode('utf-8')
				except:
					line[FullName] = ''
			# ============================================================ #
			# Parse ZIP to ZIP+ZIP4 components (when possible)
			if len(str(line[Zip])) > 5 and (str(line[Zip]).find('-') == 5):
				FullZip = line[Zip].split('-')
				line[Zip] = FullZip[0]
				line[Zip4] = FullZip[1]
			# ============================================================ #
			# Combine ZIP + CRRT
			if line[Zip] != '' and line[CRRT] != '':
				if len(str(line[Zip])) < 5:
					line[ZipCRRT] = '0' + line[Zip] + line[CRRT]
				else:
					line[ZipCRRT] = line[Zip] + line[CRRT]
			# ============================================================ #
			# Combine Address1 + Address2
			if line[AddressComb] == '' and line[Address1] != '' and \
			line[Address2] != '':
				line[AddressComb] = str.title(line[Address1]) + ' ' \
				+ str.title(line[Address2])
			elif line[Address1] != '' and line[Address2] == '':
				line[AddressComb] = str.title(line[Address1]) 
			else:
				line[AddressComb] = str.title(line[AddressComb])
			# ============================================================ #
			# Set Drop Index from Drop Dictionary and Set Customer ID	
			line[Drop] = str.upper(line[Drop])
			if line[PURL] == '':
				if str(line[ZipCRRT]) in DropDict:
					line[Drop] = DropDict[str(line[ZipCRRT])]
					if line[Drop] == 'P' or line[Drop] == 'PENNY':
						line[CustomerID] = 'P' + str(SeqNumPurchaseP)
						SeqNumPurchaseP += 1
						PennyCounter += 1
					elif line[Drop] == 'N' or line[Drop] == 'NICKEL':
						line[CustomerID] = 'N' + str(SeqNumPurchaseN)
						SeqNumPurchaseN += 1
						NickelCounter += 1
				elif line[DSF_WALK_SEQ] == '':
					line[Drop] = 'D'
					line[CustomerID] = 'D' + str(SeqNumDatabase)
					SeqNumDatabase += 1
					DatabaseCounter += 1
				elif line[DSF_WALK_SEQ] != '':
					line[Drop] = 'A'
					line[CustomerID] = 'A' + str(SeqNumPurchase)
					SeqNumPurchase += 1
					PurchaseCounter += 1
			else:
				if line[Drop] == 'P' or line[Drop] == 'PENNY':
					PennyCounter += 1
				elif line[Drop] == 'N' or line[Drop] == 'NICKEL':
					NickelCounter += 1
				elif line[Drop] == 'D':
					DatabaseCounter += 1
				elif line[Drop] == 'A':
					PurchaseCounter += 1
			# ============================================================ #
			# Parse & Format Phone #
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
			# ============================================================ #
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
			line[Make] = str.title(line[Make])
			line[Model] = str.title(line[Model])
			line[Email] = str.lower(line[Email])
			line[State] = str.upper(line[State])
			# ============================================================ #
			# Set VIN Length
			line[VINLen] = len(str(line[VIN]))
			if line[VINLen] < 17:
				line[VIN] = ''
			else:
				line[VIN] = str.upper(line[VIN])
			# ============================================================ #
			# Set SCF SCF Facility Location
			ZipLen = len(str(line[Zip]))							
			if ZipLen < 5:
				line[SCF] = (line[Zip])[:2]
			else:
				line[SCF] = (line[Zip])[:3]
			if line[SCF] in SCF3DigitDict:
				line[SCF3DFacility] = SCF3DigitDict[line[SCF]]
			# ============================================================ #
			# Set Central ZIP SCF Facility Location
			CentralZipLen = len(str(CentralZip))
			if CentralZipLen < 5:
				CentralZipSCF3Digit = str(CentralZip[:2])
			else:
				CentralZipSCF3Digit = str(CentralZip[:3])
			if CentralZipSCF3Digit in SCF3DigitDict:
				CentralZipSCFFacilityReport = SCF3DigitDict[CentralZipSCF3Digit]
			# ============================================================ #
			# Calculate Radius from Central Zip
			try:
				if CentralZip in ZipCoordinateDict:
					OriginZipCoord = ZipCoordinateDict[CentralZip]
			except:
				OriginZipCoord = ''
			try:
				if int(line[Zip][:1]) == 0:
					line[Zip] = line[Zip][-4:]
			except:
				line[Zip] = ''
			try:
				if line[Zip] in ZipCoordinateDict:
					TargetZipCoord = ZipCoordinateDict[line[Zip]]
					line[Coordinates] = TargetZipCoord
			except:
				TargetZipCoord = ''

			if OriginZipCoord == '' or TargetZipCoord == '':
				line[Radius] = 9999
			else:
				line[Radius] = round(float(vincenty(OriginZipCoord,TargetZipCoord).miles),1)
			# ============================================================ #
			# Convert "Date" Field to DateTime format
			try:
				line[Date] = parse(line[Date])
				PresentDate = parse('')
				if line[Date] == PresentDate:
					line[Date] = ''
			except:
				line[Date] = ''
			# ============================================================ #
			# Apply "Blitz-DNQ" Parameters
			try:
				if len(str(line[Phone])) < 8 or len(str(line[VIN])) < 17:
					line[BlitzDNQ] = 'dnq'
			except:
				line[BlitzDNQ] = ''
			# ============================================================ #
			# Generate "MAIL-DNQ" Tags
			# ============================================================ #
			# Apply Universal MAIL-DNQ Parameters
			if line[FirstName] == '' or line[LastName] == '' or \
			(line[Address1] == '' and line[Address2] == '') or \
			(line[City] == '') or \
			(line[State] == '') or \
			(line[Zip] == '') or \
			float(line[Radius]) > MaxRadius:
				line[MailDNQ] = 'dnq'
			# Test YEAR Validity
			try:
				YearValidityTest = int(line[Year]) # Test Year Validity
			except:
				line[Year] = ''
			if line[Year] != '':
				if str(line[Year]) in YearDecodeDict:
					line[Year] = YearDecodeDict[str(line[Year])]
				if int(line[Year]) > MaxYear or int(line[Year]) < MinYear:
					line[MailDNQ] = 'dnq'
			# Test DELDATE Validity
			try:
				line[DelDate] = parse(line[DelDate]) # Convert DateTime format
				CurrentDelDate = parse('') # Assign Current Date 
				if line[DelDate] == CurrentDelDate:
					line[DelDate] = ''
			except:
				line[DelDate] = ''
			if line[DelDate] != '':
				if int(line[DelDate].year) >= MaxSaleYear:
					line[MailDNQ] = 'dnq'
			# Process againts Suppression files
			if str.title(line[FirstName]) in DoNotMailFile or \
			str.title(line[MI]) in DoNotMailFile or \
			str.title(line[LastName]) in DoNotMailFile or \
			str.title(line[State]) in STATEList or \
			str.title(line[SCF]) in SCFList or \
			str.title(line[Year]) in YEARList or \
			str.title(line[City]) in CITYList:
				line[MailDNQ] = 'dnq'
			# ============================================================ #
			# Generate COUNTERS
			# ============================================================ #
			# Generate YEAR Counter
			if line[Year] not in YearDictCounter:
				YearDictCounter[line[Year]] = 1
			else:
				YearDictCounter[line[Year]] += 1
			# Generate MAKE Counter
			if line[Make] not in MakeDictCounter:
				MakeDictCounter[line[Make]] = 1
			else:
				MakeDictCounter[line[Make]] += 1
			# Generate SCF Counter
			if line[SCF] not in SCFDictCounter:
				SCFDictCounter[line[SCF]] = 1
			else:
				SCFDictCounter[line[SCF]] += 1
			# Generate RADIUS Counter
			if line[Radius] not in RadiusDictCounter:
				RadiusDictCounter[line[Radius]] = 1
			else:
				RadiusDictCounter[line[Radius]] += 1
			# Generate CITY Counter
			if line[City] not in CityDictCounter:
				CityDictCounter[line[City]] = 1
			else:
				CityDictCounter[line[City]] += 1
			# Generate STATE Counter
			if line[State] not in StateDictCounter:
				StateDictCounter[line[State]] = 1
			else:
				StateDictCounter[line[State]] += 1
			# Generate SCF Facility Counter
			if line[SCF3DFacility] not in SCF3DFacilityCounter:
				SCF3DFacilityCounter[line[SCF3DFacility]] = 1
			else:
				SCF3DFacilityCounter[line[SCF3DFacility]] += 1
			# Generate Zip Counter
			if line[Zip] not in ZipCounter:
				ZipCounter[line[Zip]] = 1
			else:
				ZipCounter[line[Zip]] += 1
			# ============================================================ #
			# OUTPUT Generate Phone File
			# ============================================================ #
			if line[Phone] != '' and line[BlitzDNQ] != 'dnq' and \
			line[MailDNQ] != 'dnq':
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
				HeaderRowPhonesOutput = (\
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
					OutputPhones.writerow(HeaderRowPhonesOutput)
					PhonesFirstTime = False
				else:
					OutputPhones = csv.writer(CleanOutputPhones)
					OutputPhones.writerow(HeaderRowPhonesOutput)
			# ============================================================ #
			# OUTPUT Dupes and Mail-DNQ Files
			# ============================================================ #
			key = (str.title(line[AddressComb]),str.title(line[Zip]))
			# key = (str.title(line[FirstName]),str.title(line[LastName]),str.title(line[AddressComb]),str.title(line[Zip]))
			if key not in Entries:
				if line[MailDNQ] == 'dnq':
					if MDNQFirstTime:
						OutMDNQ = csv.writer(MDNQ)
						OutMDNQ.writerow(HeaderRowMain)
						OutMDNQ.writerow(line)
						Entries.add(key)
						MDNQFirstTime = False
						MDNQCounter += 1
					else:
						OutMDNQ = csv.writer(MDNQ)
						OutMDNQ.writerow(line)
						Entries.add(key)
						MDNQCounter += 1
				else:
					if CleanOutputFirstTime:
						OutputClean = csv.writer(CleanOutput)
						OutputClean.writerow(HeaderRowMain)
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
					OutDupes.writerow(HeaderRowMain)
					OutDupes.writerow(line)
					Entries.add(key)
					DupesFirstTime = False
					DupesCounter += 1
				else:
					OutDupes = csv.writer(Dupes)
					OutDupes.writerow(line)
					Entries.add(key)
					DupesCounter += 1
			# ============================================================ #
			# Generate Suppression File
			# ============================================================ #
			if line[PURL] != '':
				HeaderRowSuppression = [\
					'First Name',\
					'Last Name',\
					'Address',\
					'City',\
					'State',\
					'Zip',\
					'Campaign Name'\
					]
				HeaderRowSuppressionOutput = (\
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
					MonthlySupp.writerow(HeaderRowSuppression)
					MonthlySupp.writerow(HeaderRowSuppressionOutput)
					MonthlySuppressionFirstTime = False
				else:
					MonthlySupp = csv.writer(AppendMonthlySupp)
					MonthlySupp.writerow(HeaderRowSuppressionOutput)
			# ============================================================ #
			# Genrate Secondary Output Files
			# ============================================================ #
			# Output Database File
			if line[DSF_WALK_SEQ] == '' and line[PURL] == '':
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
				HeaderRowDatabaseOutput = (\
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
					line[Drop]\
					)
				if DatabaseFirstTime:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(HeaderRowDatabase)
					OutputCleanDatabase.writerow(HeaderRowDatabaseOutput)
					DatabaseFirstTime = False
				else:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(HeaderRowDatabaseOutput)
			
			# Output Purchase File
			elif line[DSF_WALK_SEQ] != '' and line[PURL] == '':
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
				HeaderRowPurchaseOutput = (\
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
					line[Drop]\
					)
				if PurchaseFirstTimeAll:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchase)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchaseOutput)
					PurchaseFirstTimeAll = False
				else:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchaseOutput)
			
			# Output Appended files [ Penny / Nickel / Other ]
			else:
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
				HeaderRowAppendOutput = (\
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
					line[Drop]\
					)
				if line[CustomerID][:1] == 'P' or line[CustomerID][:1] == 'p':
					if AppendFirstTimeP:
						OutputCleanAppendP = csv.writer(CleanOutputAppendP)
						OutputCleanAppendP.writerow(HeaderRowAppend)
						OutputCleanAppendP.writerow(HeaderRowAppendOutput)
						AppendFirstTimeP = False
					else:
						OutputCleanAppendP = csv.writer(CleanOutputAppendP)
						OutputCleanAppendP.writerow(AppendOutputHeader)
				elif line[CustomerID][:1] == 'N' or line[CustomerID][:1] == 'n':
					if AppendFirstTimeN:
						OutputCleanAppendN = csv.writer(CleanOutputAppendN)
						OutputCleanAppendN.writerow(HeaderRowAppend)
						OutputCleanAppendN.writerow(HeaderRowAppendOutput)
						AppendFirstTimeN = False
					else:
						OutputCleanAppendN = csv.writer(CleanOutputAppendN)
						OutputCleanAppendN.writerow(HeaderRowAppendOutput)
				else: 
					if AppendFirstTimeR:
						OutputCleanAppendR = csv.writer(CleanOutputAppendR)
						OutputCleanAppendR.writerow(HeaderRowAppend)
						OutputCleanAppendR.writerow(HeaderRowAppendOutput)
						AppendFirstTimeR = False
					else:
						OutputCleanAppendR = csv.writer(CleanOutputAppendR)
						OutputCleanAppendR.writerow(HeaderRowAppendOutput)
# ==================================================================== #
if __name__ == '__main__':
	# ============================================================ #
	# Function
	# ============================================================ #
	def upkeep():
		# Clean up temporary files
		Files = glob.glob('*.csv')
		for Record in Files:
			if os.path.getsize(Record) == 0:
				os.remove(Record)
			if bool(re.match('.+Re-Mapped.+',Record,flags=re.I)):
				os.remove(Record)

	def percentage(part, whole):
		if whole == 0:
			return 0
		else:
			return 100 * float(part)/float(whole)
	# ============================================================ #
	main() # Main Function
	RadiusRTotal = 0
	YearRTotal = 0
	CityRTotal = 0
	SCFRTotal = 0
	StateRTotal = 0
	MakeRTotal = 0
	DelDateRTotal = 0
	SCFFacilityRTotal = 0
	ZIPRTotal = 0
	SortedSCFText = ''
	# ============================================================ #
	# Output Report
	Report = sys.stdout
	with open('SUMMARY-REPORT_' + IPFName + '.md','w') as Log:
		sys.stdout =  Log
		print('')
		print('-------------------------------------')
		print('#### DATA SUMMARY REPORT')
		print('-------------------------------------')
		print('|Category|Description|')
		print('|-:|:-|')
		print('|Project Name|{}|'.format(IPFName))
		print('|Central ZIP Code|{}|'.format(CentralZip))
		print('|SCF Facility|{}|'.format(CentralZipSCFFacilityReport))
		print('|Max Radius|{} Miles|'.format(MaxRadius))
		print('|Max Year|{}|'.format(MaxYear))
		print('|Min Year|{}|'.format(MinYear))
		print('|Max DelDate Year|{}|'.format(MaxSaleYear))
		print('|||')
		print('|Database Total|**{}**|'.format(DatabaseCounter))
		print('|Purchase Total|**{}**|'.format(PurchaseCounter))
		print('|Penny Total|**{}**|'.format(PennyCounter))
		print('|Nickel Total|**{}**|'.format(NickelCounter))
		print('|Less MDNQ Total|**({})**|'.format(MDNQCounter))
		print('|Less Dupes Total|**({})**|'.format(DupesCounter))
		GrandTotal = DatabaseCounter + PurchaseCounter + PennyCounter + NickelCounter - MDNQCounter - DupesCounter
		print('|**GRAND TOTAL**|**{}**|'.format(GrandTotal))
		print('')
		SUBTotal = DatabaseCounter + PurchaseCounter + PennyCounter + NickelCounter
		# ============================================================ #
		# TOP Counts
		# ============================================================ #
		print('-------------------------------------')
		print('#### TOP Counts')
		print('-------------------------------------')
		print('')
		print('##### TOP Counts by STATE ( >5% ):')
		print('||State|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(StateDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			StateRTotal = StateRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, StateRTotal, round(Prcnt,1)))
		print('')		
		print('##### TOP Counts by SCF ( >5% ):')
		print('||SCF|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(SCFDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			SCFRTotal = SCFRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, SCFRTotal, round(Prcnt,1)))
		print('')
		for key in sorted(SCFDictCounter.iterkeys()):
			SortedSCFText = SortedSCFText + str(key) + ' | '
		print('<!--')
		print(SortedSCFText)
		print('-->')
		print('')
		print('##### TOP Counts by SCF FACILITY ( >5% ):')
		print('||SCF Facility|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(SCF3DFacilityCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			SCFFacilityRTotal = SCFFacilityRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, SCFFacilityRTotal, round(Prcnt,1)))
		print('')
		print('##### TOP Counts by YEAR ( >5% ):')
		print('||Year|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key in sorted(YearDictCounter.iterkeys(), reverse = True):
			YearRTotal = YearRTotal + YearDictCounter[key]
			Prcnt = percentage(YearDictCounter[key], SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, YearDictCounter[key], YearRTotal, round(Prcnt,1)))
		print('')
		print('##### TOP Counts by RADIUS ( >5% ):')
		print('||Radius|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key in sorted(RadiusDictCounter.iterkeys()):
			RadiusRTotal = RadiusRTotal + RadiusDictCounter[key]
			Prcnt = percentage(RadiusDictCounter[key], SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, RadiusDictCounter[key], RadiusRTotal, round(Prcnt,1)))
		print('')
		print('##### TOP Counts by CITY ( >5% ):')
		print('||City|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(CityDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			CityRTotal = CityRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, CityRTotal, round(Prcnt,1)))
		print('')
		print('##### TOP Counts by ZIP ( >5% ):')
		print('||SCF|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(ZipCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			ZIPRTotal = ZIPRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, ZIPRTotal, round(Prcnt,1)))
		print('')
		print('##### TOP Counts by MAKE ( >5% ):')
		print('||Make|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(MakeDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			MakeRTotal = MakeRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, MakeRTotal, round(Prcnt,1)))
		print('')
		# ============================================================ #
		# Distributions
		# ============================================================ #
		print('-------------------------------------')
		print('#### Distributions')
		print('-------------------------------------')
		print('')
		StateRTotal = 0
		SCFRTotal = 0
		SCFFacilityRTotal = 0
		YearRTotal = 0
		RadiusRTotal = 0
		CityRTotal = 0
		MakeRTotal = 0
		ZIPRTotal = 0
		print('##### Count Distribution by STATE:')
		print('||State|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(StateDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			StateRTotal = StateRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, StateRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, value, StateRTotal, round(Prcnt,1)))
		print('')
		print('##### Count Distribution by SCF:')
		print('||SCF|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(SCFDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			SCFRTotal = SCFRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, SCFRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, value, SCFRTotal, round(Prcnt,1)))
		print('')
		print('##### Count Distribution by SCF FACILITY:')
		print('||SCFFacility|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(SCF3DFacilityCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			SCFFacilityRTotal = SCFFacilityRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, SCFFacilityRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, value, SCFFacilityRTotal, round(Prcnt,1)))
		print('')
		print('##### Count Distribution by YEAR:')
		print('||Year|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key in sorted(YearDictCounter.iterkeys(), reverse = True):
			YearRTotal = YearRTotal + YearDictCounter[key]
			Prcnt = percentage(YearDictCounter[key], SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, YearDictCounter[key], YearRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, YearDictCounter[key], YearRTotal, round(Prcnt,1)))
		print('')
		print('##### Count Distribution by RADIUS:')
		print('||Radius|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key in sorted(RadiusDictCounter.iterkeys()):
			RadiusRTotal = RadiusRTotal + RadiusDictCounter[key]
			Prcnt = percentage(RadiusDictCounter[key], SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, RadiusDictCounter[key], RadiusRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, RadiusDictCounter[key], RadiusRTotal, round(Prcnt,1)))
		print('')
		print('##### Count Distribution by CITY:')
		print('||City|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(CityDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			CityRTotal = CityRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, CityRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, value, CityRTotal, round(Prcnt,1)))
		print('')
		print('##### TOP Counts by ZIP ( >5% ):')
		print('||SCF|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(ZipCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			ZIPRTotal = ZIPRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, ZIPRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, value, ZIPRTotal, round(Prcnt,1)))
		print('')
		print('##### Count Distribution by MAKE:')
		print('||Make|Count|RTotal|%|')
		print('||-|-:|-:|-:|')
		for key, value in sorted(MakeDictCounter.iteritems(), key = lambda (k,v): (v,k), reverse = True):
			MakeRTotal = MakeRTotal + value
			Prcnt = percentage(value, SUBTotal)
			if Prcnt > 5:
				print('|**>**|**{}**|**{}**|{}|{}%|'.format(key, value, MakeRTotal, round(Prcnt,1)))
			else:
				print('||{}|{}|{}|{}%|'.format(key, value, MakeRTotal, round(Prcnt,1)))
		print('')
		sys.stdout = Report
	print('---------------------------------------')
	print('............. T O T A L ............. : {}'.format(GrandTotal))
	print('---------------------------------------')
	print('          C O M P L E T E D            ')
	print('')
	upkeep() # Call upkeep Function
	# ============================================================ #
