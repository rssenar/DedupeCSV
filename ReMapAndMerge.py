#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, glob, re
from tqdm import tqdm
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
FirstTime = True
NewHeaderRowFirstTime = True
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------
Selection = raw_input("Merge Files? [Y/N]: ")
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
Misc1 = 35
Misc2 = 36
Misc3 = 37

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
		elif bool(re.search('4Z.+',field,flags=re.I)):
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
		open('_ReMapped_' + str(CSVFiles[index]),'ab') as OutputFile:
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

def MultiFileMarge():
	CSVFilesHaveHeaderRow = True
	FirstFileUseHeaderRow = True
	CSVFiles = glob.glob('_*.csv')
	for line in CSVFiles:
		with open(line,'rU') as File, open('__MergeFile.csv','ab') as Merge:
			File = open(line,'rU')
			OutputClean = csv.writer(Merge)
			Input = csv.reader(File)
			if FirstFileUseHeaderRow == True:
				for line in tqdm(Input):
					OutputClean.writerow(line)
				FirstFileUseHeaderRow = False
			else:
				FirstLine = True
				for line in tqdm(Input):
					if CSVFilesHaveHeaderRow and FirstLine:
						FirstLine = False
					else:
						OutputClean.writerow(line)
# ---------------------------------------------
ReMapHeaderFields()
# ---------------------------------------------
if Selection == 'Y' or Selection == 'y':
	MultiFileMarge()
