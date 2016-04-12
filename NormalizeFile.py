
#!/usr/bin/env python3.4.3
# ---------------------------------------------------------------------------- #
import csv, os, sys, glob, collections, datetime, subprocess
from dateutil.parser import *
from Constants import *
from geopy.distance import vincenty
from nameparser import HumanName
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
CSVFile = glob.glob('*.csv')
recpath = '../Dropbox/HUB/Projects/PyToolkit/Resources'
DropFile = os.path.join(recpath,'_DropFile.csv')
GenSuppressionFile = os.path.join(recpath,'_GeneralSuppression.csv')
MonthlySuppressionFile = os.path.join(recpath,'_MonthlySuppression.csv')
ZipCoordFile = os.path.join(recpath,'USZIPCoordinates.csv')
SCF3DigitFile = os.path.join(recpath,'SCFFacilites.csv')
Entries = set()
# ---------------------------------------------------------------------------- #
# Select processing Mode
SuppSelect = str.upper(input(
	'Select Mode... (B)asic | (S)tandard: '
	))
while SuppSelect != 'S' and SuppSelect != 'B':
	SuppSelect = str.upper(input(
		'ERROR! Enter Valid Selection... : '
		))
if SuppSelect == 'B':
	print('=======================================')
	print('             B  A  S  I  C             ')
	print('=======================================')
else:
	SuppSelect = 'S'
	print('=======================================')
	print('         S  T  A  N  D  A  R  D        ')
	print('=======================================')
# ---------------------------------------------------------------------------- #
# Select Input File from Database
for file in CSVFile:
	IPFName = file.strip('.csv')
	InputFile = file
# ---------------------------------------------------------------------------- #
# Import Drop Dictionary from Drop_File.csv file
try:
	DropDict = {}
	with open(DropFile,'rU') as DropFile:
		DropRec = csv.reader(DropFile)
		next(DropFile)
		for line in DropRec:
			DropDict[line[0]] = line[1]
except:
	print('..... ERROR: Unable to Load Drop Dictionary File')
# ---------------------------------------------------------------------------- #
# Import General Suppression File
if SuppSelect == 'S':
	try:
		with open(GenSuppressionFile,'rU') as GenSuppressionFile:
			GenSuppression = csv.reader(GenSuppressionFile)
			next(GenSuppressionFile)
			for line in GenSuppression:
				Entries.add((str.title(line[2]),str.title(line[5])))
	except:
		print('..... ERROR: Unable to Load GENERAL Suppression File')
else:
	print('... General Suppression File Not Loaded')
# ---------------------------------------------------------------------------- #
# Import Montly Suppression File
if SuppSelect == 'S':
	try:
		with open(MonthlySuppressionFile,'rU') as MonthlySuppressionFile:
			MonthlySuppression = csv.reader(MonthlySuppressionFile)
			next(MonthlySuppressionFile)
			for line in MonthlySuppression:
				Entries.add((str.title(line[2]),str.title(line[5])))
	except:
		print('..... ERROR: Unable to Load Montly Suppression File')
else:
	print('... Monthly Suppression File Not Loaded')
# ---------------------------------------------------------------------------- #
# Import Zip Dictionary from US_ZIP_Coordinates.csv file
try:
	ZipCoordinateDict = {}
	with open(ZipCoordFile,'rU') as ZipCoord:
		ZipCoordinate = csv.reader(ZipCoord)
		for line in ZipCoordinate:
			ZipCoordinateDict[line[0]] = (line[1], line[2])
except:
	print('..... ERROR: Unable to Load Zip Dictionary File')
# ---------------------------------------------------------------------------- #
# Import Mail DNQ File for the purposes of de-duping
if SuppSelect != 'S':
	DoNotMailSet = set()
	print('.............. Mail DNQ File Not Loaded')
# ---------------------------------------------------------------------------- #
# Import SCF Dictionary from SCF Facilities.csv file
try:
	SCF3DigitDict = {}
	with open(SCF3DigitFile,'rU') as SCF3DigitFile:
		SCF3Digit = csv.reader(SCF3DigitFile)
		for line in SCF3Digit:
			SCF3DigitDict[line[0]] = (line[1])
except:
	print('..... ERROR: Unable to Load SCF 3-Digit Dictionary File')
# ---------------------------------------------------------------------------- #
# Function to Convert String To List
def ConvertStringToList(input):
	AppendedList = []
	input = input.split('|')
	for item in input:
		item = item.strip()
		item = str.lower(item)
		AppendedList.append(item)
	return AppendedList
# ---------------------------------------------------------------------------- #
# Function to Reformat Phone Number and strip white space and extra char
def ReformatPhoneNum(Phone):
	Phone = str(Phone).strip()
	Phone = str(Phone).replace('-','')
	Phone = str(Phone).replace('(','')
	Phone = str(Phone).replace(')','')
	return Phone
# ---------------------------------------------------------------------------- #
# Counter Function
def GenCounter(record, DictCntr):
	if str(record) not in DictCntr:
		DictCntr[str(record)] = 1
	else:
		DictCntr[str(record)] += 1
# ---------------------------------------------------------------------------- #
# Function to Generate Percentage
def percentage(part, whole):
	if whole == 0:
		return 0
	else:
		return 100 * float(part)/float(whole)
# ---------------------------------------------------------------------------- #
# Convert list item to string
def ConvListToString(input):
	for item in input:
		return item
# ---------------------------------------------------------------------------- #
# Remove temporary files
def Upkeep():
	Files = glob.glob('*.csv')
	for Record in Files:
		if os.path.getsize(Record) == 0: # Empty files
			os.remove(Record)
		if bool(re.match('.+Re-Mapped.+', Record, flags = re.I)):
			os.remove(Record)
# ---------------------------------------------------------------------------- #
# Print captured input file
print('File Name ........................... : {}'.format(InputFile))
CentralZip = input(
	'Enter Central ZIP Code .............. : '
	).strip()
while str(CentralZip) not in ZipCoordinateDict:
	CentralZip = input(
		'ERROR: Enter ZIP Codes............... : '
		).strip()

# Capture Input - Max RADIUS
if SuppSelect == 'S':
	try:
		MaxRadius = int(input(
			'Enter MAX Radius ................[50] : '
			).strip())
	except:
		MaxRadius = 50
else:
	MaxRadius = 9999

# Capture Input - Max YEAR
if SuppSelect == 'S':
	try:
		MaxYear = int(input(
			'Enter MAX Year ................[2014] : '
			).strip())
	except:
		MaxYear = 2014
else:
	MaxYear = 9999

# Capture Input - Min YEAR
if SuppSelect == 'S':
	try:
		MinYear = int(input(
			'Enter MIN Year ................[1990] : '
			).strip())
	except:
		MinYear = 1990
else:
	MinYear = 1

# Capture Input - Max SALE YEAR
if SuppSelect == 'S':
	try:
		MaxSaleYear = int(input(
			'Enter SOLD Years up to ........[2014] : '
			).strip())
	except:
		MaxSaleYear = 2014
else:
	MaxSaleYear = 9999

# Generate Suppress STATE List
if SuppSelect == 'S':
	STATEList = input(
		'Enter Suppression List .......[STATE] : '
		)
	if STATEList != '':
		STATEList = sorted(ConvertStringToList(STATEList))
		print('..STATEList : {}'.format(STATEList))
	else:
		STATEList = []
else:
	STATEList = []

# Generate Suppress SCF List
if SuppSelect == 'S':
	SCFList = input(
		'Enter Suppression List .........[SCF] : '
		)
	if SCFList != '':
		SCFList = sorted(ConvertStringToList(SCFList))
		print('....SCFList : {}'.format(SCFList))
	else:
		SCFList = []
else:
	SCFList = []

# Generate Suppress YEAR List
if SuppSelect == 'S':
	YEARList = input(
		'Enter Suppression List ........[YEAR] : '
		)
	if YEARList != '':
		YEARList = sorted(ConvertStringToList(YEARList))
		print('...YEARList : {}'.format(YEARList))
	else:
		YEARList = []
else:
	YEARList = []

# Generate Suppress CITY List
if SuppSelect == 'S':
	CITYList = input(
		'Enter Suppression List ........[CITY] : '
		)
	if CITYList != '':
		CITYList = sorted(ConvertStringToList(CITYList))
		print('...CITYList : {}'.format(CITYList))
	else:
		CITYList =[]
else:
	CITYList =[]

# Set TOP Percentage
if SuppSelect == 'S':
	TOPPercentage = input(
		'Set Top % .......................[3%] : '
		).strip()
	try:
		TOPPercentage = int(TOPPercentage)
	except:
		TOPPercentage = 3
else:
	TOPPercentage = 0

# Import LOCAL Suppression File for the purposes of de-duping
SuppressionFileName = input(
	'Enter Suppression File Name ......... : '
	).strip()
SuppressionFile = '{}.csv'.format(SuppressionFileName)
if SuppressionFileName != '':
	try:
		with open(SuppressionFile,'rU') as SuppressionFile:
			Suppression = csv.reader(SuppressionFile)
			next(SuppressionFile)
			for line in Suppression:
				Entries.add((str.title(line[2]),str.title(line[5])))
			print('\n{}.csv File Loaded\n'.format(SuppressionFileName))
	except:
		print('ERROR: Cannot load local suppression file\n')
else:
	print('     No Suppression File Selected     ')

# Set Vendor Selection
if SuppSelect == 'S':
	VendorSelect = str.upper(input(
		'....... (S)hopper | (P)latinum .......'
		).strip())
else:
	VendorSelect = ''
input('       PRESS [ENTER] TO PROCEED        ')
# ---------------------------------------------------------------------------- #
ReMappedOutput = '>>>>>>>>>> Re-Mapped <<<<<<<<<<.csv'
Dupes = '>>>>>>>>>> Dupes <<<<<<<<<<.csv'
MDNQ = '>>>>>>>>>> M-DNQ <<<<<<<<<<.csv'
CleanOutput = '{}_UpdatedOutputMain.csv'.format(IPFName)
AppendMonthlySuppFile = '{}_AddMonthlySuppression.csv'.format(IPFName)
CleanOutputPhones = '{}_PHONES.csv'.format(IPFName)
CleanOutputDatabase = '{}_UPLOAD DATA.csv'.format(IPFName)
CleanOutputPurchaseAll = '{}_UPLOAD.csv'.format(IPFName)
CleanOutputAppendP = '{}_PENNY.csv'.format(IPFName)
CleanOutputAppendN = '{}_NICKEL.csv'.format(IPFName)
CleanOutputAppendR = '{}_OTHER.csv'.format(IPFName)
# ---------------------------------------------------------------------------- #
# Compare File Header row to HeaderRowMain to determin if re-mapping required
ExtractCSVHeader = subprocess.check_output(['head','-n','1',InputFile])
ExtractCSVHeader = ExtractCSVHeader.decode("utf-8").split(',')
ExtractCSVHeader = [x.replace("\r\n","") for x in ExtractCSVHeader]
if ExtractCSVHeader == HeaderRowMain:
	HRSelect = 'N'
else:
	HRSelect = 'Y'
# ---------------------------------------------------------------------------- #
# Function to re-map header rows and transpose csv data
def ReMapFunc():
	if HRSelect == 'Y':
		print('------------- RE-MAPPING -------------')
		global Selection
		Selection = ReMappedOutput
		with open(InputFile,'rU') as InputFileReMap,\
		open(ReMappedOutput,'at') as ReMappedOutputFile:
			Input = csv.reader(InputFileReMap)
			Output = csv.writer(ReMappedOutputFile)
			Output.writerow(HeaderRowMain)
			FirstLine = True
			for line in tqdm(Input):
				if FirstLine:
					for IndexA in range(0,len(line)):
						MatchHeaderFields(line[IndexA], IndexA)
					FirstLine = False
				else:
					newline = []
					for IndexB in range(0,len(HeaderRowMain)):
						if IndexB in HeaderDict:
							newline.append(eval(HeaderDict[IndexB]))
						else:
							newline.append('')
					Output.writerow(newline)
	else:
		Selection = InputFile
# ---------------------------------------------------------------------------- #
# Main function to normalize file
def NormalizeFunc():
	print('------------- NORMALIZING ------------')
	global CentralZip
	global CentralZipSCFFacilityReport
	global CityDictCounter
	global CleanOutput
	global CleanOutputAppendN
	global CleanOutputAppendP
	global CleanOutputAppendR
	global CleanOutputDatabase
	global CleanOutputPhones
	global CleanOutputPurchaseAll
	global DatabaseCounter
	global Dupes
	global DupesCounter
	global MakeDictCounter
	global MaxSaleYear
	global MDNQ
	global MDNQCounter
	global NickelCounter
	global PennyCounter
	global PurchaseCounter
	global RadiusDictCounter
	global SCF3DFacilityCounter
	global SCFDictCounter
	global SeqNumDatabase
	global SeqNumPurchase
	global SeqNumPurchaseN
	global SeqNumPurchaseP
	global StateDictCounter
	global TOPPercentage
	global VendorSelected
	global YearDictCounter
	with open(Selection,'rU') as InputFile,\
	open(CleanOutput,'at') as CleanOutput,\
	open(Dupes,'at') as Dupes,\
	open(MDNQ,'at') as MDNQ,\
	open(CleanOutputPhones,'at') as CleanOutputPhones,\
	open(CleanOutputDatabase,'at') as CleanOutputDatabase,\
	open(CleanOutputPurchaseAll,'at') as CleanOutputPurchaseAll,\
	open(CleanOutputAppendP,'at') as CleanOutputAppendP,\
	open(CleanOutputAppendN,'at') as CleanOutputAppendN,\
	open(CleanOutputAppendR,'at') as CleanOutputAppendR,\
	open(AppendMonthlySuppFile,'at') as AppendMonthlySupp:
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
		YearDictCounter = {}
		MakeDictCounter = {}
		ModelDictCounter = {}
		SCFDictCounter = {}
		RadiusDictCounter = {}
		CityDictCounter = {}
		StateDictCounter = {}
		SCF3DFacilityCounter = {}
		ZipCounter = {}
		PennyCounter = 0
		NickelCounter = 0
		DatabaseCounter = 0
		PurchaseCounter = 0
		MDNQCounter = 0
		DupesCounter = 0
		Input = csv.reader(InputFile)
		next(InputFile)
		for line in tqdm(Input):
			if VendorSelect == 'P':
				WinningNumber = 42619 # Platinum
				line[Vendor] = 'Platinum'
			elif VendorSelect == 'S':
				WinningNumber = 40754 # Shopper
				line[Vendor] = 'Shopper'
			else:
				WinningNumber = 40754 # Default
				line[Vendor] = 'Premierworks'
			line[WinningNum] = WinningNumber
			VendorSelected = line[Vendor] 
			
			# Parse Fullname if First & Last Name fields are missing
			if line[FullName] != '' and \
			line[FirstName] == '' and line[LastName] == '':
				try:
					ParsedFName = HumanName(str.title(line[FullName]))
					line[FirstName] = ParsedFName.first
					line[MI] = ParsedFName.middle
					line[LastName] = ParsedFName.last
				except:
					line[FullName] = ''
			
			# Parse ZIP to ZIP & ZIP4 components (when possible)
			if len(str(line[Zip])) > 5 and (str(line[Zip]).find('-') == 5):
				FullZip = line[Zip].split('-')
				line[Zip] = FullZip[0]
				line[Zip4] = FullZip[1]
			
			# Combine ZIP + CRRT fields
			if line[Zip] != '' and line[CRRT] != '':
				if len(str(line[Zip])) < 5:
					line[ZipCRRT] = '0{}{}'.format(
						line[Zip],
						line[CRRT]
						)
				else:
					line[ZipCRRT] = '{}{}'.format(
						line[Zip],
						line[CRRT]
						)
			
			# Combine Address1 + Address2
			if line[AddressComb] == '' and\
			line[Address1] != '' and\
			line[Address2] != '':
				line[AddressComb] = '{} {}'.format(
					str.title(line[Address1]),
					str.title(line[Address2])
					)
			elif line[Address1] != '' and line[Address2] == '':
				line[AddressComb] = str.title(line[Address1]) 
			else:
				line[AddressComb] = str.title(line[AddressComb])
			
			# Set Drop Index from Drop Dictionary and Set Customer ID	
			if line[PURL] == '':
				if str(line[ZipCRRT]) in DropDict:
					line[Drop] = DropDict[str(line[ZipCRRT])]
					if line[Drop] == 'P' or line[Drop] == 'Penny' or\
					line[Drop] == 'p' or line[Drop] == 'penny':
						line[CustomerID] = 'P{}'.format(
							str(SeqNumPurchaseP)
							)
						SeqNumPurchaseP += 1
						PennyCounter += 1
					elif line[Drop] == 'N' or line[Drop] == 'Nickel' or\
					line[Drop] == 'n' or line[Drop] == 'nickel':
						line[CustomerID] = 'N{}'.format(
							str(SeqNumPurchaseN)
							)
						SeqNumPurchaseN += 1
						NickelCounter += 1
				elif line[DSF_WALK_SEQ] == '':
					line[Drop] = 'D'
					line[CustomerID] = 'D{}'.format(
						str(SeqNumDatabase)
						)
					SeqNumDatabase += 1
					DatabaseCounter += 1
				elif line[DSF_WALK_SEQ] != '':
					line[Drop] = 'A'
					line[CustomerID] = 'A{}'.format(
						str(SeqNumPurchase)
						)
					SeqNumPurchase += 1
					PurchaseCounter += 1
			else:
				if line[Drop] == 'P' or line[Drop] == 'Penny' or\
				line[Drop] == 'p' or line[Drop] == 'penny':
					PennyCounter += 1
				elif line[Drop] == 'N' or line[Drop] == 'Nickel' or\
				line[Drop] == 'n' or line[Drop] == 'nickel':
					NickelCounter += 1
				elif line[Drop] == 'D':
					DatabaseCounter += 1
				elif line[Drop] == 'A':
					PurchaseCounter += 1
			
			# Parse & Clean up Phone #
			if line[MPhone] != '' and len(str(line[MPhone])) > 6:
				line[Phone] = ReformatPhoneNum(line[MPhone])
			elif line[HPhone] != '' and len(str(line[HPhone])) > 6:
				line[Phone] = ReformatPhoneNum(line[HPhone])
			elif line[WPhone] != '' and len(str(line[WPhone])) > 6:
				line[Phone] = ReformatPhoneNum(line[WPhone])
			else:
				line[Phone] = ''
			
			# Re-Format Phone#
			if len(str(line[Phone])) == 10:
				line[Phone] = '({}) {}-{}'.format(
					str(line[Phone][0:3]),
					str(line[Phone][3:6]),
					str(line[Phone][6:10])
					)
			elif len(str(line[Phone])) == 7:
				line[Phone] = '{}-{}'.format(
					str(line[Phone][0:3]),
					str(line[Phone][3:7])
					)
			else:
				line[Phone] = ''
			
			# Set Case for data fields
			line[FullName] = str.title(line[FullName])
			line[FirstName] = str.title(line[FirstName])
			if len(str(line[MI])) == 1:
				line[MI] = str.upper(line[MI])
			elif len(str(line[MI])) > 1:
				line[MI] = str.title(line[MI])
			else:
				line[MI] = ''
			line[LastName] = str.title(line[LastName])
			line[Address1] = str.title(line[Address1])
			line[Address2] = str.title(line[Address2])
			line[City] = str.title(line[City])
			line[Make] = str.title(line[Make])
			line[Model] = str.title(line[Model])
			line[Email] = str.lower(line[Email])
			line[State] = str.upper(line[State])
			
			# Set VIN Length
			line[VINLen] = len(str(line[VIN]))
			if line[VINLen] < 17:
				line[VIN] = ''
			else:
				line[VIN] = str.upper(line[VIN])
			
			# Set SCF Facility Location
			ZipLen = len(str(line[Zip]))				
			if ZipLen < 5:
				line[SCF] = (line[Zip])[:2]
			else:
				line[SCF] = (line[Zip])[:3]
			if str(line[SCF]) in SCF3DigitDict:
				line[SCF3DFacility] = SCF3DigitDict[str(line[SCF])]
			
			# Set Central ZIP SCF Facility location
			CentralZipLen = len(str(CentralZip))
			if CentralZipLen < 5:
				CentralZipSCF3Digit = str(CentralZip[:2])
			else:
				CentralZipSCF3Digit = str(CentralZip[:3])
			if str(CentralZipSCF3Digit) in SCF3DigitDict:
				CentralZipSCFFacilityReport = SCF3DigitDict[str(CentralZipSCF3Digit)]
			
			# Calculate RADIUS from CENTRAL ZIP
			try:
				line[Zip] = int(line[Zip])
			except:
				line[Zip] = 9999
			
			# Remove Leading 0 from Zip Code
			if str(line[Zip])[:1] == 0 and len(str(line[Zip])) == 4:
				line[Zip] = line[Zip][-4:]
			
			# Set Long & Lat Coordinates for Central Zip Code and Zip Code
			OriginZipCoord = ZipCoordinateDict[str(CentralZip)]
			if str(line[Zip]) in ZipCoordinateDict:
				line[Coordinates] = ZipCoordinateDict[str(line[Zip])]
			else:
				line[Coordinates] = ''
			
			# Set RADIUS
			if line[Coordinates] == '':
				line[Radius] = 9999.9999
			else:
				line[Radius] = vincenty(OriginZipCoord,line[Coordinates]).miles
				line[Radius] = round(float(line[Radius]),2)
			
			# Convert DATE Field to DateTime format
			try:
				line[Date] = parse(line[Date])
				PresentDate = parse('')
				if line[Date] == PresentDate:
					line[Date] = ''
			except:
				line[Date] = ''
			
			# Apply "Blitz-DNQ" Parameters
			try:
				if len(str(line[Phone])) < 8 and len(str(line[VIN])) < 17:
					line[BlitzDNQ] = 'dnq'
			except:
				line[BlitzDNQ] = ''
			
			# Apply Universal MAIL-DNQ Parameters
			if line[FirstName] == '' or line[LastName] == '' or\
			(line[Address1] == '' and line[Address2] == '') or\
			(line[City] == '') or\
			(line[State] == '') or\
			(line[Zip] == '') or\
			float(line[Radius]) > MaxRadius:
				line[MailDNQ] = 'dnq'
			
			# Test YEAR Validity
			try:
				YearValidityTest = int(line[Year])
				if int(line[Year]) in YearDecodeDict:
					line[Year] = YearDecodeDict[int(line[Year])]
				if int(line[Year]) > MaxYear:
					line[MailDNQ] = 'dnq'
				if int(line[Year]) < MinYear:
					line[MailDNQ] = 'dnq'
			except:
				line[Year] = 'N/A'
						
			# Set 'N/A' for MAKE & MODEL blank fields
			if line[Make] == '':
				line[Make] = 'N/A'
			if line[Model] == '':
				line[Model] = 'N/A'

			# Test DELDATE Validity
			try:
				line[DelDate] = parse(line[DelDate])
				CurrentDelDate = parse('')
				if line[DelDate] == CurrentDelDate:
					line[DelDate] = ''
				if int(line[DelDate].year) > MaxSaleYear:
					line[MailDNQ] = 'dnq'
			except:
				line[DelDate] = ''
			
			# Dedupe againts suppression files
			if str.lower(line[FirstName]) in DoNotMailSet or\
			str.lower(line[MI]) in DoNotMailSet or\
			str.lower(line[LastName]) in DoNotMailSet or\
			str.lower(line[State]) in STATEList or\
			str.lower(line[SCF]) in SCFList or\
			str(line[Year]) in YEARList or\
			str.lower(line[City]) in CITYList:
				line[MailDNQ] = 'dnq'
						
			# Generate COUNTERS
			CityRadius = '{} {} ({} Miles)'.format(
				line[City],
				line[Zip],
				line[Radius]
				)
			ZipRadius = '{} ({} Miles)'.format(
				line[Zip],
				line[Radius]
				)
			GenCounter(line[Year],YearDictCounter)
			GenCounter(line[Make],MakeDictCounter)
			GenCounter(line[SCF],SCFDictCounter)
			GenCounter(line[Radius],RadiusDictCounter)
			GenCounter(CityRadius,CityDictCounter)
			GenCounter(line[State],StateDictCounter)
			GenCounter(line[SCF3DFacility],SCF3DFacilityCounter)
			GenCounter(ZipRadius,ZipCounter)
			
			# OUTPUT Generate Phone File
			if line[Phone] != '' and\
			line[BlitzDNQ] != 'dnq' and\
			line[MailDNQ] != 'dnq':
				HeaderRowPhonesStat = [
					'First Name',
					'Last Name',
					'Phone',
					'Address',
					'City',
					'State',
					'Zip',
					'Last Veh Year',
					'Last Veh Make',
					'Last Veh Model'
					]
				HeaderRowPhonesOutput = (
					line[FirstName],
					line[LastName],
					line[Phone],
					line[AddressComb],
					line[City],
					line[State],
					line[Zip],
					line[Year],
					line[Make],
					line[Model]
					)
				if PhonesFirstTime:
					OutputPhones = csv.writer(CleanOutputPhones)
					OutputPhones.writerow(HeaderRowPhonesStat)
					OutputPhones.writerow(HeaderRowPhonesOutput)
					PhonesFirstTime = False
				else:
					OutputPhones = csv.writer(CleanOutputPhones)
					OutputPhones.writerow(HeaderRowPhonesOutput)
			
			# OUTPUT Dupes and Mail-DNQ Files
			key = (str.title(line[AddressComb]), str(line[Zip]))
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
			
			# Generate Suppression File
			if line[PURL] != '':
				HeaderRowSuppressionStat = [
					'First Name',
					'Last Name',
					'Address',
					'City',
					'State',
					'Zip',
					'Campaign Name'
					]
				HeaderRowSuppressionOutput = (
					line[FirstName],
					line[LastName],
					line[AddressComb],
					line[City],
					line[State],
					line[Zip],
					IPFName
					)
				if MonthlySuppressionFirstTime:
					MonthlySupp = csv.writer(AppendMonthlySupp)
					MonthlySupp.writerow(HeaderRowSuppressionStat)
					MonthlySupp.writerow(HeaderRowSuppressionOutput)
					MonthlySuppressionFirstTime = False
				else:
					MonthlySupp = csv.writer(AppendMonthlySupp)
					MonthlySupp.writerow(HeaderRowSuppressionOutput)
			
			# Output Database File
			if line[DSF_WALK_SEQ] == '' and line[PURL] == '':
				HeaderRowDatabaseStat = [
					'Customer ID',
					'First Name',
					'Last Name',
					'Address',
					'City',
					'State',
					'Zip',
					#'Phone',
					#'Year',
					#'Make',
					#'Model',
					'Winning Number',
					'Position'
					]
				HeaderRowDatabaseOutput = (
					line[CustomerID],
					line[FirstName],
					line[LastName],
					line[AddressComb],
					line[City],
					line[State],
					line[Zip],
					#line[Phone],
					#line[Year],
					#line[Make],
					#line[Model],
					line[WinningNum],
					line[Drop]
					)
				if DatabaseFirstTime:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(HeaderRowDatabaseStat)
					OutputCleanDatabase.writerow(HeaderRowDatabaseOutput)
					DatabaseFirstTime = False
				else:
					OutputCleanDatabase = csv.writer(CleanOutputDatabase)
					OutputCleanDatabase.writerow(HeaderRowDatabaseOutput)
			
			# Output Purchase File
			elif line[DSF_WALK_SEQ] != '' and line[PURL] == '':
				HeaderRowPurchaseStat = [
					'Customer ID',
					'First Name',
					'Last Name',
					'Address',
					'City',
					'State',
					'Zip',
					'4Zip',
					'DSF_WALK_SEQ',
					'Crrt',
					'Winning Number',
					'Position'
					]
				HeaderRowPurchaseOutput = (
					line[CustomerID],
					line[FirstName],
					line[LastName],
					line[AddressComb],
					line[City],
					line[State],
					line[Zip],
					line[Zip4],
					line[DSF_WALK_SEQ],
					line[CRRT],
					line[WinningNum],
					line[Drop]
					)
				if PurchaseFirstTimeAll:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchaseStat)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchaseOutput)
					PurchaseFirstTimeAll = False
				else:
					OutputCleanPurchaseAll = csv.writer(CleanOutputPurchaseAll)
					OutputCleanPurchaseAll.writerow(HeaderRowPurchaseOutput)
			
			# Output Appended files [Penny/Nickel/Other]
			else:
				HeaderRowAppendStat = [
					'PURL',
					'First Name',
					'Last Name',
					'Address1',
					'City',
					'State',
					'Zip',
					'4Zip',
					'Crrt',
					'DSF_WALK_SEQ',
					'Customer ID',
					'Position'
					]
				HeaderRowAppendOutput = (
					line[PURL],
					line[FirstName],
					line[LastName],
					line[Address1],
					line[City],
					line[State],
					line[Zip],
					line[Zip4],
					line[CRRT],
					line[DSF_WALK_SEQ],
					line[CustomerID],
					line[Drop]
					)
				if line[CustomerID][:1] == 'P' or line[CustomerID][:1] == 'p':
					if AppendFirstTimeP:
						OutputCleanAppendP = csv.writer(CleanOutputAppendP)
						OutputCleanAppendP.writerow(HeaderRowAppendStat)
						OutputCleanAppendP.writerow(HeaderRowAppendOutput)
						AppendFirstTimeP = False
					else:
						OutputCleanAppendP = csv.writer(CleanOutputAppendP)
						OutputCleanAppendP.writerow(HeaderRowAppendOutput)
				elif line[CustomerID][:1] == 'N' or line[CustomerID][:1] == 'n':
					if AppendFirstTimeN:
						OutputCleanAppendN = csv.writer(CleanOutputAppendN)
						OutputCleanAppendN.writerow(HeaderRowAppendStat)
						OutputCleanAppendN.writerow(HeaderRowAppendOutput)
						AppendFirstTimeN = False
					else:
						OutputCleanAppendN = csv.writer(CleanOutputAppendN)
						OutputCleanAppendN.writerow(HeaderRowAppendOutput)
				else: 
					if AppendFirstTimeR:
						OutputCleanAppendR = csv.writer(CleanOutputAppendR)
						OutputCleanAppendR.writerow(HeaderRowAppendStat)
						OutputCleanAppendR.writerow(HeaderRowAppendOutput)
						AppendFirstTimeR = False
					else:
						OutputCleanAppendR = csv.writer(CleanOutputAppendR)
						OutputCleanAppendR.writerow(HeaderRowAppendOutput)
# ---------------------------------------------------------------------------- #
# Function to generate output file 
def OutputFileFunc():
	Report = sys.stdout
	with open('SUMMARY-REPORT_{}.md'.format(IPFName),'w') as Log:
		RadiusKeyList = sorted(RadiusDictCounter)
		NewRadiusList = []
		for item in RadiusKeyList:
			NewRadiusList.append(float(item))
		HighestRadius = ConvListToString(sorted(NewRadiusList)[-1:])
		HigherstYear = ConvListToString(sorted(YearDictCounter)[-1:])
		LowestYear = ConvListToString(sorted(YearDictCounter)[:1])
		TodayDateTime = datetime.datetime.now()
		GrandTotal = (DatabaseCounter + PurchaseCounter + PennyCounter
			+ NickelCounter - MDNQCounter - DupesCounter)
		SUBTotal = (DatabaseCounter + PurchaseCounter
			+ PennyCounter + NickelCounter)
		sys.stdout = Log
		print()
		print('------------------------------------------------------------')
		print('#### {}'.format(str.upper(IPFName)))
		print('###### Data Summary Report - as of {}'.format(TodayDateTime))
		print('------------------------------------------------------------')
		print()
		print('||Description|')
		print('|-:|:-|')
		print('|Central ZIP Code|{}|'.format(CentralZip))
		print('|SCF Facility|{}|'.format(CentralZipSCFFacilityReport))
		print('|Max Radius|{} Miles|'.format(HighestRadius))
		print('|Max Year|{}|'.format(HigherstYear))
		print('|Min Year|{}|'.format(LowestYear))
		print('|Sold Years up to|{}|'.format(MaxSaleYear))
		print('|Vendor|{}|'.format(VendorSelected))
		print('|Database Total|{}|'.format(DatabaseCounter))
		print('|Purchase Total|{}|'.format(PurchaseCounter))
		print('|Penny Total|{}|'.format(PennyCounter))
		print('|Nickel Total|{}|'.format(NickelCounter))
		print('|Less MDNQ Total|({})|'.format(MDNQCounter))
		print('|Less Dupes Total|({})|'.format(DupesCounter))
		print('|**GRAND TOTAL**|**{}**|'.format(GrandTotal))
		print()
		print('------------------------------------------------------------')
		print('###### Count Distribution by STATE:')
		print('||State|Count|%|RTotal|%|')
		print('||-|-:|-:|-:|-:|')
		StateRTotal = 0
		OdStateDictCounter = collections.OrderedDict(sorted(
			StateDictCounter.items(), key=lambda t: t[0], reverse = True
			))
		for key, value in OdStateDictCounter.items():
			StateRTotal = StateRTotal + value
			ValuePrcnt = percentage(value, SUBTotal)
			RTotalPrcnt = percentage(StateRTotal, SUBTotal)
			if ValuePrcnt > TOPPercentage:
				print('|>|{}|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					StateRTotal,
					round(RTotalPrcnt,2)
					))
			else:
				print('||{}|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					StateRTotal,
					round(RTotalPrcnt,2)
					))
		print()
		print('###### Count Distribution by SCF FACILITY and 3-Digit:')
		print('||SCF Facilities|Count|%|RTotal|%|')
		print('||-|-:|-:|-:|-:|')
		SCFFacilityRTotal = 0
		OdSCF3DFacilityCounter = collections.OrderedDict(sorted(
			SCF3DFacilityCounter.items(), key=lambda t: t[1], reverse = True
			))
		for key, value in OdSCF3DFacilityCounter.items():
			SCFFacilityRTotal = SCFFacilityRTotal + value
			ValuePrcnt = percentage(value, SUBTotal)
			RTotalPrcnt = percentage(SCFFacilityRTotal, SUBTotal)
			if ValuePrcnt > TOPPercentage:
				print('|>|{}|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					SCFFacilityRTotal,
					round(RTotalPrcnt,2)
					))
			else:
				print('||{}|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					SCFFacilityRTotal,
					round(RTotalPrcnt,2)
					))
		print()
		print('||3-Digit|Count|%|RTotal|%|')
		print('||-|-:|-:|-:|-:|')
		SCFRTotal = 0
		OdSCFDictCounter = collections.OrderedDict(sorted(
			SCFDictCounter.items(), key=lambda t: t[1], reverse = True
			))
		for key, value in OdSCFDictCounter.items():
			SCFRTotal = SCFRTotal + value
			ValuePrcnt = percentage(value, SUBTotal)
			RTotalPrcnt = percentage(SCFRTotal, SUBTotal)
			if ValuePrcnt > TOPPercentage:
				if len(str(key)) == 2:
					print('|>|0{}|{}|{}%|{}|{}%|'.format(
						key,
						value,
						round(ValuePrcnt,2),
						SCFRTotal,
						round(RTotalPrcnt,2)
						))
				else:
					print('|>|{}|{}|{}%|{}|{}%|'.format(
						key,
						value,
						round(ValuePrcnt,2),
						SCFRTotal,
						round(RTotalPrcnt,2)
						))
			else:
				if len(str(key)) == 2:
					print('||0{}|{}|{}%|{}|{}%|'.format(
						key,
						value,
						round(ValuePrcnt,2),
						SCFRTotal,
						round(RTotalPrcnt,2)
						))
				else:
					print('||{}|{}|{}%|{}|{}%|'.format(
						key,
						value,
						round(ValuePrcnt,2),
						SCFRTotal,
						round(RTotalPrcnt,2)
						))
		print()
		SortedSCFText = ''
		OdSCFDictCounter = collections.OrderedDict(sorted(
			SCFDictCounter.items(), key=lambda t: t[0]
			))
		for key, value in OdSCFDictCounter.items():
			SortedSCFText = '{} {} |'.format(
				SortedSCFText,
				key
				)
		print('<!--',SortedSCFText,'-->')
		print()	
		if len(YearDictCounter) !=  1:
			print('###### Count Distribution by YEAR:')
			print('||Years|Count|%|RTotal|%|')
			print('||-|-:|-:|-:|-:|')
			YearRTotal = 0
			OdYearDictCounter = collections.OrderedDict(sorted(
				YearDictCounter.items(), key=lambda t: t[0], reverse = True
				))
			for key, value in OdYearDictCounter.items():
				YearRTotal = YearRTotal + value
				ValuePrcnt = percentage(value, SUBTotal)
				RTotalPrcnt = percentage(YearRTotal, SUBTotal)
				if ValuePrcnt > TOPPercentage:
					print('|>|{}|{}|{}%|{}|{}%|'.format(
						key,
						value,
						round(ValuePrcnt,2),
						YearRTotal,
						round(RTotalPrcnt,2)
						))
				else:
					print('||{}|{}|{}%|{}|{}%|'.format(
						key,
						value,
						round(ValuePrcnt,2),
						YearRTotal,
						round(RTotalPrcnt,2)
						))
			print()
		print('###### Count Distribution by RADIUS:')
		print('||Radius|Count|%|RTotal|%|')
		print('||-|-:|-:|-:|-:|')
		RadiusRTotal = 0
		OdRadiusDictCounter = collections.OrderedDict(sorted(
			RadiusDictCounter.items(), key=lambda t: float(t[0])
			))
		for key, value in OdRadiusDictCounter.items():
			RadiusRTotal = RadiusRTotal + value
			ValuePrcnt = percentage(value, SUBTotal)
			RTotalPrcnt = percentage(RadiusRTotal, SUBTotal)
			if ValuePrcnt > TOPPercentage:
				print('|>|{} Miles|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					RadiusRTotal,
					round(RTotalPrcnt,2)
					))
			else:
				print('||{} Miles|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					RadiusRTotal,
					round(RTotalPrcnt,2)
					))
		print()
		if len(MakeDictCounter) !=  1:
			print('###### Top Counts by MAKE ( > {}% ):'.format(TOPPercentage))
			print('||Makes|Count|%|RTotal|%|')
			print('||-|-:|-:|-:|-:|')
			MakeRTotal = 0
			OdMakeDictCounter = collections.OrderedDict(sorted(
				MakeDictCounter.items(), key=lambda t: t[1], reverse = True
				))
			for key, value in OdMakeDictCounter.items():
				MakeRTotal = MakeRTotal + value
				ValuePrcnt = percentage(value, SUBTotal)
				RTotalPrcnt = percentage(MakeRTotal, SUBTotal)
				if ValuePrcnt > TOPPercentage:
					print('|>|{}|{}|{}%|{}|{}%|'.format(
						key,
						value,
						round(ValuePrcnt,2),
						MakeRTotal,
						round(RTotalPrcnt,2)
						))
			print()
		print('###### Top Counts & Distributions by CITY ( > {}% ):'.format(TOPPercentage))
		print('||Top Cities|Count|%|RTotal|')
		print('||-|-:|-:|-:|')
		CityRTotal = 0
		OdCityDictCounter = collections.OrderedDict(sorted(
			CityDictCounter.items(), key=lambda t: t[1], reverse = True
			))
		for key, value in OdCityDictCounter.items():
			CityRTotal = CityRTotal + value
			ValuePrcnt = percentage(value, SUBTotal)
			if ValuePrcnt > TOPPercentage:
				print('|>|{}|{}|{}%|{}|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					CityRTotal
					))
		print()
		print('||Cities|Count|%|RTotal|%|')
		print('||-|-:|-:|-:|-:|')
		CityRTotal = 0
		OdCityDictCounter = collections.OrderedDict(sorted(
			CityDictCounter.items(), key=lambda t: t[0]
			))
		for key, value in OdCityDictCounter.items():
			CityRTotal = CityRTotal + value
			ValuePrcnt = percentage(value, SUBTotal)
			RTotalPrcnt = percentage(CityRTotal, SUBTotal)
			if ValuePrcnt > TOPPercentage:
				print('|>|{}|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					CityRTotal,
					round(RTotalPrcnt,2)
					))
			else:
				print('||{}|{}|{}%|{}|{}%|'.format(
					key,
					value,
					round(ValuePrcnt,2),
					CityRTotal,
					round(RTotalPrcnt,2)
					))
		sys.stdout = Report
	print('================ TOTAL ================ : {}'.format(GrandTotal))
	print('=====  C  O  M  P  L  E  T  E  D  =====')
	print('=======================================')
	print()
	Upkeep()
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
	ReMapFunc()
	NormalizeFunc()
	OutputFileFunc()
