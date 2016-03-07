
#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, glob, re
from tqdm import tqdm
# ---------------------------------------------
os.chdir('../../../../Desktop/')

CSVFilesHaveHeaderRow = True
CleanOutputFirstTime = True
DatabaseFirstTime = True
PurchaseFirstTime = True
PurchaseFirstTimeP = True
PurchaseFirstTimeN = True
PhonesFirstTime = True
DupesFirstTime = True
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
# ---------------------------------------------
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------
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
		elif bool(re.search(r'\b4zip\b',field,flags=re.I)) or\
			bool(re.search(r'\bzip4\b',field,flags=re.I)) :
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
	for index in range(0,len(CSVFiles)):
		global i
		global x
		with open(CSVFiles[index],'rU') as InputFile,\
		open('__ReMapped_' + str(CSVFiles[index]),'ab') as OutputFile:
			Input = csv.reader(InputFile)
			Output = csv.writer(OutputFile)
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

def Split():
	FirstFileUseHeaderRow = True
	CSVFiles = glob.glob('__*.csv')
	for Files in CSVFiles:
		for line in Files:
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
				#line[BuybackValues],\
				line[WinningNum],\
				line[DropVal]\
				)
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
				#line[Phone],\
				line[CRRT],\
				line[WinningNum],\
				line[DropVal]\
				)
		
			global PurchaseFirstTimeP
			global PurchaseFirstTimeN
			global PurchaseFirstTime
			global CleanOutputPurchaseP
			global CleanOutputPurchaseN
			global CleanOutputPurchase
					
			if (line[CustomerID])[:1] == 'p' or (line[CustomerID])[:1] == 'P': 
				if PurchaseFirstTimeP:
					CleanOutputPurchaseP = open('Penny_' + str(Files),'ab')
					OutputCleanPurchaseP = csv.writer(CleanOutputPurchaseP)
					OutputCleanPurchaseP.writerow(HeaderRowPurchase)
					OutputCleanPurchaseP.writerow(PurchaseOutputHeader)
					PurchaseFirstTimeP = False
				else:
					OutputCleanPurchaseP = csv.writer(CleanOutputPurchaseP)
					OutputCleanPurchaseP.writerow(PurchaseOutputHeader)
			elif (line[CustomerID])[:1] == 'n' or (line[CustomerID])[:1] == 'N': 
				if PurchaseFirstTimeN:
					CleanOutputPurchaseN = open('Nikel_' + str(Files),'ab')
					OutputCleanPurchaseN = csv.writer(CleanOutputPurchaseN)
					OutputCleanPurchaseN.writerow(HeaderRowPurchase)
					OutputCleanPurchaseN.writerow(PurchaseOutputHeader)
					PurchaseFirstTimeN = False
				else:
					OutputCleanPurchaseN = csv.writer(CleanOutputPurchaseN)
					OutputCleanPurchaseN.writerow(PurchaseOutputHeader)
			else:
				if PurchaseFirstTime:
					CleanOutputPurchase = open(Files,'ab')
					OutputCleanPurchase = csv.writer(CleanOutputPurchase)
					OutputCleanPurchase.writerow(HeaderRowPurchase)
					OutputCleanPurchase.writerow(PurchaseOutputHeader)
					PurchaseFirstTime = False
				else:
					OutputCleanPurchase = csv.writer(CleanOutputPurchase)
					OutputCleanPurchase.writerow(PurchaseOutputHeader)

# ---------------------------------------------
ReMapHeaderFields()
Split()
# ---------------------------------------------


