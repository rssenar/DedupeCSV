#!/usr/bin/env python
# ==================================================================== #
from __future__ import division, print_function
import csv, os, sys, re, glob
import datetime
from geopy.distance import vincenty
from dateutil.parser import *
from tqdm import tqdm
from nameparser import HumanName
# ==================================================================== #
def main():
	global CleanOutputPD
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
	global IPFName
	global CentralZip
	global MaxRadius
	global MaxYear
	global MinYear
	global CurrentDateUpdate
	global MaxSaleYear
	global CentralZipSCFFacility
	# ==================================================================== #
	os.chdir('../../../../Desktop/')
	path = '../Dropbox/HUB/Projects/PremWorks/_Resources'
	MDNQFile = os.path.join(path,'MailDNQ.csv')
	DropFile = os.path.join(path,'DropFile.csv')
	ZipCoordFile = os.path.join(path,'USZIPCoordinates.csv')
	YearDecodeFile = os.path.join(path,'YearDecode.csv')
	GenSuppressionFile = os.path.join(path,'GeneralSuppression.csv')
	MonthlySuppressionFile = os.path.join(path,'MonthlySuppression.csv')
	SCF3DigitFile = os.path.join(path,'SCFFacilites.csv')
	# ==================================================================== #
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
	Entries = set()
	DoNotMailFile = set()
	# ==================================================================== #
	def SplitAndStripFunc(input):
		AppendedList = []
		input = input.split(",")
		for item in input:
			item = item.strip()
			AppendedList.append(item)
		return AppendedList
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
	# Import GENERAL Suppression File for the purposes of de-duping
	try:
		with open(GenSuppressionFile,'rU') as GenSuppressionFile:
			GenSuppression = csv.reader(GenSuppressionFile)
			for line in GenSuppression:
				Entries.add((str.title(line[2]),str.title(line[5])))
	except:
		print('ERROR: Unable to Load GENERAL Suppression File')
	# Import Montly Suppression File for the purposes of de-duping
	try:
		with open(MonthlySuppressionFile,'rU') as MonthlySuppressionFile:
			MonthlySuppression = csv.reader(MonthlySuppressionFile)
			for line in MonthlySuppression:
				Entries.add((str.title(line[2]),str.title(line[5])))
	except:
		print('ERROR: Unable to Load Montly Suppression File')
	# Import Mail DNQ File for the purposes of de-duping
	try:
		with open(MDNQFile,'rU') as MDNQFile:
			MDNQ = csv.reader(MDNQFile)
			for line in MDNQ:
				DoNotMailFile.add(line[0])
	except:
		print('ERROR: Unable to Load Mail DNQ File')
	# Import Drop Dictionary from Drop_File.csv file
	try:
		DropDict = {}
		with open(DropFile,'rU') as DropFile:
			Drop = csv.reader(DropFile)
			for line in Drop:
				DropDict[line[0]] = line[1]
	except:
		print('ERROR: Unable to Load Drop Dictionary File')
	# Import Year Decode Dictionary from Year_Decode.csv file
	try:
		YearDecodeDict = {}
		with open(YearDecodeFile,'rU') as YearDecodeFile:
			YearDecode = csv.reader(YearDecodeFile)
			for line in YearDecode:
				YearDecodeDict[line[0]] = (line[1])
	except:
		print('ERROR: Unable to Load Year Decode Dictionary File')
	# Import SCF Dictionary from SCF Facilities.csv file
	try:
		SCF3DigitDict = {}
		with open(SCF3DigitFile,'rU') as SCF3DigitFile:
			SCF3Digit = csv.reader(SCF3DigitFile)
			for line in SCF3Digit:
				SCF3DigitDict[line[0]] = (line[1])
	except:
		print('ERROR: Unable to Load SCF 3-Digit Dictionary File')
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
		MaxYear = int(raw_input('Enter Max Year ................[2014] : '))
	except:
		MaxYear = 2014
	# Capture Input - Min YEAR
	try:
		MinYear = int(raw_input('Enter Min Year ................[1990] : '))
	except:
		MinYear = 1990
	# Capture Input - Max SALE YEAR
	try:
		MaxSaleYear = int(raw_input('Enter Maximum Sales Year ......[2015] : '))
	except:
		MaxSaleYear = 2015
	# Generate Suppress STATE List
	STATEList = raw_input('Enter Suppression List .......[STATE] : ')
	if STATEList != '':
		STATEList = SplitAndStripFunc(STATEList)
		print('STATEList = ', STATEList)
	else:
		STATEList = []
		print('STATEList = ', STATEList)
	# Generate Suppress SCF List
	SCFList = raw_input('Enter Suppression List .........[SCF] : ')
	if SCFList != '':
		SCFList = SplitAndStripFunc(SCFList)
		print('SCFList = ', SCFList)
	else:
		SCFList = []
		print('SCFList = ', SCFList)
	# Generate Suppress YEAR List
	YEARList = raw_input('Enter Suppression List ........[YEAR] : ')
	if YEARList != '':
		YEARList = SplitAndStripFunc(YEARList)
		print('YEARList = ', YEARList)
	else:
		YEARList = []
		print('YEARList = ', YEARList)
	# Generate Suppress CITY List
	CITYList = raw_input('Enter Suppression List ........[CITY] : ')
	if CITYList != '':
		CITYList = SplitAndStripFunc(CITYList)
		print('CITYList = ', CITYList)
	else:
		CITYList =[]
		print('CITYList = ', CITYList)
	# Import LOCAL Suppression File for the purposes of de-duping
	SuppressionFileName = raw_input('Enter Suppression File ....[OPTIONAL] : ')
	SuppressionFile = SuppressionFileName + '.csv'
	if SuppressionFileName != '':
		try:
			with open(SuppressionFile,'rU') as SuppressionFile:
				Suppression = csv.reader(SuppressionFile)
				for line in Suppression:
					Entries.add((str.title(line[2]),str.title(line[5])))
		except:
			print('     ERROR: Cannot load local suppression file')
	# Capture ReMap Header Row Selection
	HRSelect = raw_input('......ReMap Header Row? [Default = N] : ')
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
	SCF3DigitAddr = 38
	Misc1 = 39
	Misc2 = 40
	Misc3 = 41
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
		'SCF3DigitAddr',\
		'Misc1',\
		'Misc2',\
		'Misc3'\
		]
	# ==================================================================== #
	# ReMap Header
	if HRSelect == 'Y' or HRSelect == 'y':
		Selection = ReMappedOutput
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
				HeaderDict[Drop] = 'line['+str(i)+']'
			elif bool(re.search(r'\bpurl\b',field,flags=re.I)):
				HeaderDict[PURL] = 'line['+str(i)+']'
			elif bool(re.search(r'\byrdec\b',field,flags=re.I)):
				HeaderDict[YrDec] = 'line['+str(i)+']'		
			elif bool(re.search(r'\bSCF3DigitAddr\b',field,flags=re.I)):
				HeaderDict[SCF3DigitAddr] = 'line['+str(i)+']'
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
		# ---------------------------
		YearDictCounter = {}
		MakeDictCounter = {}
		ModelDictCounter = {}
		SCFDictCounter = {}
		RadiusDictCounter = {}
		CityDictCounter = {}
		StateDictCounter = {}
		# ---------------------------
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
			# Parse ZIP code to ZIP + ZIP4 components
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
			if line[PURL] == '':
				if line[ZipCRRT] in DropDict:
					line[Drop] = DropDict[line[ZipCRRT]]
					if line[Drop] == 'P' or line[Drop] == 'p' or \
					line[Drop] == 'Penny' or line[Drop] == 'penny':
						line[CustomerID] = 'p' + str(SeqNumPurchaseP)
						SeqNumPurchaseP += 1
						PennyCounter += 1
					elif line[Drop] == 'N' or line[Drop] == 'n' or \
					line[Drop] == 'Nickel' or line[Drop] == 'nickel':
						line[CustomerID] = 'n' + str(SeqNumPurchaseN)
						SeqNumPurchaseN += 1
						NickelCounter += 1
				elif line[DSF_WALK_SEQ] == '':
					line[Drop] = 'd'
					line[CustomerID] = 'd' + str(SeqNumDatabase)
					SeqNumDatabase += 1
					DatabaseCounter += 1
				elif line[DSF_WALK_SEQ] != '':
					line[Drop] = 'a'
					line[CustomerID] = 'a' + str(SeqNumPurchase)
					SeqNumPurchase += 1
					PurchaseCounter += 1
			else:
				if line[Drop] == 'P' or line[Drop] == 'p' or \
				line[Drop] == 'Penny' or line[Drop] == 'penny':
					PennyCounter += 1
				elif line[Drop] == 'N' or line[Drop] == 'n' or \
				line[Drop] == 'Nickel' or line[Drop] == 'nickel':
					NickelCounter += 1
				elif line[Drop] == 'd':
					DatabaseCounter += 1
				elif line[Drop] == 'a':
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
			# Assign Year Decode Field
			try:
				if str(line[Year]) in YearDecodeDict:
					line[YrDec] = YearDecodeDict[line[Year]]
			except:
				line[YrDec] = ''
			# ============================================================ #
			# Set SCF & Central ZIP SCF 3Digit Address
			ZipLen = len(str(line[Zip]))				
			try:
				if ZipLen < 5:
					line[SCF] = (line[Zip])[:2]
				else:
					line[SCF] = (line[Zip])[:3]
				if line[SCF] in SCF3DigitDict:
					line[SCF3DigitAddr] = SCF3DigitDict[line[SCF]]
			except:
				line[SCF3DigitAddr] = ''
			# ============================================================ #
			# Set SCF Facility Location from Central ZIP	
			CentralZipLen = len(str(CentralZip))
			if CentralZipLen < 5:
				CentralZipSCF3Digit = str(CentralZip[:2])
			else:
				CentralZipSCF3Digit = str(CentralZip[:3])
			try:
				if CentralZipSCF3Digit in SCF3DigitDict:
					line[SCF3DigitAddr] = SCF3DigitDict[CentralZipSCF3Digit]
					CentralZipSCFFacility = line[SCF3DigitAddr]
			except:
				line[SCF3DigitAddr] = ''
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
				if int(line[Year]) > MaxYear or int(line[Year]) < MinYear:
					line[MailDNQ] = 'dnq'
			except:
				line[MailDNQ] = 'dnq'
			# Test DELDATE Validity
			try:
				line[DelDate] = parse(line[DelDate]) # Convert DateTime format
				CurrentDelDate = parse('') # Assign Current Date 
				if line[DelDate] == CurrentDelDate:
					line[DelDate] = ''
		
				DelDateYear = int(line[DelDate].year) # Extract YEAR parameter
				if int(line[DelDate].year) >= MaxSaleYear:
					line[MailDNQ] = 'dnq'
			except:
				line[DelDate] = ''
			# Process againts Suppression files
			if str(line[FirstName]) in DoNotMailFile or \
			str(line[MI]) in DoNotMailFile or \
			str(line[LastName]) in DoNotMailFile or \
			str(line[State]) in STATEList or \
			str(line[SCF]) in SCFList or \
			str(line[Year]) in YEARList or \
			str(line[City]) in CITYList:
				line[MailDNQ] = 'dnq'
			# ============================================================ #
			# Generate COUNTERS
			# ============================================================ #
			if line[Year] not in YearDictCounter: # Generate YEAR Counter
				YearDictCounter[line[Year]] = 1
			else:
				YearDictCounter[line[Year]] += 1
			if line[Make] not in MakeDictCounter: # Generate MAKE Counter
				MakeDictCounter[line[Make]] = 1
			else:
				MakeDictCounter[line[Make]] += 1
			if line[SCF] not in SCFDictCounter: # Generate SCF Counter
				SCFDictCounter[line[SCF]] = 1
			else:
				SCFDictCounter[line[SCF]] += 1
			if line[Radius] not in RadiusDictCounter: # Generate RADIUS Counter
				RadiusDictCounter[line[Radius]] = 1
			else:
				RadiusDictCounter[line[Radius]] += 1	
			if line[City] not in CityDictCounter: # Generate CITY Counter
				CityDictCounter[line[City]] = 1
			else:
				CityDictCounter[line[City]] += 1
			if line[State] not in StateDictCounter: # Generate STATE Counter
				StateDictCounter[line[State]] = 1
			else:
				StateDictCounter[line[State]] += 1
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
			# ============================================================ #
			# OUTPUT Dupes and Mail-DNQ Files
			# ============================================================ #
			key = (line[AddressComb],line[Zip])
			# key = (line[FirstName],line[LastName],line[AddressComb],line[Zip])
			if key not in Entries:
				if line[MailDNQ] == 'dnq':
					if MDNQFirstTime:
						OutMDNQ = csv.writer(MDNQ)
						OutMDNQ.writerow(HeaderRow)
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
			# ============================================================ #
			# Genrate Secondary Output Database File
			# ============================================================ #
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
					line[Drop]\
					)
				if DatabaseFirstTime:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(HeaderRowDatabase)
					OutputCleanDatabase.writerow(DatabaseOutputHeader)
					DatabaseFirstTime = False
				else:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(DatabaseOutputHeader)
			# ============================================================ #
			# Generate Secondary Output Purchase
			# ============================================================ #
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
					line[Drop]\
					)
				if PurchaseFirstTimeAll:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchase)
					OutputCleanPurchaseAll.writerow(PurchaseOutputHeader)
					PurchaseFirstTimeAll = False
				else:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(PurchaseOutputHeader)
			# ============================================================ #
			# Generate Append Output File
			# ============================================================ #
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
					line[Drop]\
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
		# ==================================================================== #

if __name__ == '__main__':
	# ============================================================ #
	def Upkeep():
		# Clean up temporary files
		Files = glob.glob('*.csv')
		for Record in Files:
			if os.path.getsize(Record) == 0:
				os.remove(Record)
			if bool(re.match('.+Re-Mapped.+',Record,flags=re.I)):
				os.remove(Record)
	# ============================================================ #
	try:
		main() # Call Main Function
		RadiusRTotal = 0
		YearRTotal = 0
		CityRTotal = 0
		SCFRTotal = 0
		StateRTotal = 0
		MakeRTotal = 0
		DelDateRTotal = 0
		# Output Log Report
		Report = sys.stdout
		with open('Summary_Report_Log.txt','w') as Log:
			sys.stdout =  Log
			print('')
			print('=====================================')
			print('SUMMARY REPORT LOG')
			print('=====================================')
			print('Project Name.........: {}'.format(IPFName))
			print('Central ZIP Code.....: {}'.format(CentralZip))
			print('SCF Facility.........: {}'.format(CentralZipSCFFacility))
			print('Max Radius...........: {} Miles'.format(MaxRadius))
			print('Max Year.............: {}'.format(MaxYear))
			print('Min Year.............: {}'.format(MinYear))
			print('Max DelDate Year.....: {}'.format(MaxSaleYear))
			print('')
			print('   DATABASE Total....: {}'.format(DatabaseCounter))
			print('   PURCHASE Total....: {}'.format(PurchaseCounter))
			print('      PENNY Total....: {}'.format(PennyCounter))
			print('     NICKEL Total....: {}'.format(NickelCounter))
			print('  Less MDNQ Total....: ({})'.format(MDNQCounter))
			print(' Less DUPES Total....: ({})'.format(DupesCounter))
			print('')
			print('=====================================')
			print('GRAND TOTAL..........: {} Records'.format(DatabaseCounter + \
			PurchaseCounter + PennyCounter + NickelCounter - \
			MDNQCounter - DupesCounter))
			print('=====================================')
			print('STATE Distribution + RTotal:')
			for key, value in sorted(StateDictCounter.iteritems(), \
				key = lambda (k,v): (v,k), reverse = True):
				StateRTotal = StateRTotal + value
				print('  {}....: {} [{}]'.format(key, value, StateRTotal))
			print('')
			print('SCF Distribution + RTotal:')
			for key, value in sorted(SCFDictCounter.iteritems(), \
				key = lambda (k,v): (v,k), reverse = True):
				SCFRTotal = SCFRTotal + value
				print('  SCF {}....: {} [{}]'.format(key, value, SCFRTotal))
			print('')
			print('YEAR Distribution + RTotal:')
			for key in sorted(YearDictCounter.iterkeys(), reverse = True):
				YearRTotal = YearRTotal + YearDictCounter[key]
				print('  Yr {}....: {} [{}]'.format(key, YearDictCounter[key], \
					YearRTotal))
			print('')
			print('RADIUS Distribution + RTotal:')
			for key in sorted(RadiusDictCounter.iterkeys()):
				RadiusRTotal = RadiusRTotal + RadiusDictCounter[key]
				print('  {} Miles....: {} [{}]'.format(key, RadiusDictCounter[key], \
					RadiusRTotal))
			print('')
			print('CITY Distribution + RTotal:')
			for key, value in sorted(CityDictCounter.iteritems(), \
				key = lambda (k,v): (v,k), reverse = True):
				CityRTotal = CityRTotal + value
				print('  {}....: {} [{}]'.format(key, value, CityRTotal))
			print('')
			print('MAKE Distribution + RTotal:')
			for key, value in sorted(MakeDictCounter.iteritems(), \
				key = lambda (k,v): (v,k), reverse = True):
				MakeRTotal = MakeRTotal + value
				print('  {}....: {} [{}]'.format(key, value, MakeRTotal))
			print('')
			sys.stdout = Report
		print('=======================================')
		print('............. T O T A L ............. : {}'.format(DatabaseCounter + \
			PurchaseCounter + PennyCounter + NickelCounter - \
			MDNQCounter - DupesCounter))
		print('=======================================')
		Upkeep() # Call Upkeep Function
		print('========= C O M P L E T E D! ==========')
		print('=======================================')
	except:
		print('CRITICAL ERROR! Process Terminated')
		print('')
		Upkeep() # Call Upkeep Function
		
