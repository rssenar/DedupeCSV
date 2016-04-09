
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import csv, os, glob, re
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------------------------------------- #
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
Vendor = 39
Misc1 = 40
Misc2 = 41
Misc3 = 42

# Header Output list
HeaderRowMain = [
	'CustomerID',
	'FullName',
	'FirstName',
	'MI',
	'LastName',
	'Address1',
	'Address2',
	'AddressFull',
	'City',
	'State',
	'Zip',
	'4Zip',
	'SCF',
	'Phone',
	'HPH',
	'BPH',
	'CPH',
	'Email',
	'VIN',
	'Year',
	'Make',
	'Model',
	'DelDate',
	'Date',
	'Radius',
	'Coordinates',
	'VINLen',
	'DSF_WALK_SEQ',
	'Crrt',
	'ZipCrrt',
	'KBB',
	'BuybackValue',
	'WinningNumber',
	'MailDNQ',
	'BlitzDNQ',
	'Drop',
	'PURL',
	'YrDec',
	'SCF3DFacility',
	'Vendor',
	'Misc1',
	'Misc2',
	'Misc3'
	]
# ---------------------------------------------------------------------------- #
# Re-Map Column Fields
def ReMapHeaderFields():
	HeaderDict = {}
	def match(field):
		if bool(re.search('cus.+id',field,flags=re.I)):
			HeaderDict[CustomerID] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('ful.+me',field,flags=re.I)):
			HeaderDict[FullName] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('fir.+me',field,flags=re.I)):
			HeaderDict[FirstName] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bmi\b',field,flags=re.I)):
			HeaderDict[MI] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('las.+me',field,flags=re.I)):
			HeaderDict[LastName] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('addr.+1',field,flags=re.I)):
			HeaderDict[Address1] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('addr.+2',field,flags=re.I)):
			HeaderDict[Address2] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('addr.+full',field,flags=re.I)):
			HeaderDict[AddressComb] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bcity\b',field,flags=re.I)):
			HeaderDict[City] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bstate\b',field,flags=re.I)):
			HeaderDict[State] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bzip\b',field,flags=re.I)):
			HeaderDict[Zip] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\b4zip\b',field,flags=re.I)) or \
		bool(re.search(r'\bzip4\b',field,flags=re.I)):
			HeaderDict[Zip4] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bscf\b',field,flags=re.I)):
			HeaderDict[SCF] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('pho.+',field,flags=re.I)):
			HeaderDict[Phone] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('HPho.+',field,flags=re.I)) or \
		bool(re.search(r'\bhph\b',field,flags=re.I)):
			HeaderDict[HPhone] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('WPho.+',field,flags=re.I)) or \
		bool(re.search(r'\bbph\b',field,flags=re.I)):
			HeaderDict[WPhone] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('MPho.+',field,flags=re.I)) or \
		bool(re.search(r'\bcph\b',field,flags=re.I)):
			HeaderDict[MPhone] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bemail\b',field,flags=re.I)):
			HeaderDict[Email] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bvin\b',field,flags=re.I)):
			HeaderDict[VIN] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\byear\b',field,flags=re.I)) or \
		bool(re.search(r'\bvyr\b',field,flags=re.I)):
			HeaderDict[Year] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bmake\b',field,flags=re.I)) or \
		bool(re.search(r'\bvmk\b',field,flags=re.I)):
			HeaderDict[Make] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bmodel\b',field,flags=re.I)) or \
		bool(re.search(r'\bvmd\b',field,flags=re.I)):
			HeaderDict[Model] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bdeldate\b',field,flags=re.I)):
			HeaderDict[DelDate] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bdate\b',field,flags=re.I)):
			HeaderDict[Date] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bradius\b',field,flags=re.I)):
			HeaderDict[Radius] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('coord.+',field,flags=re.I)):
			HeaderDict[Coordinates] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bvinlen\b',field,flags=re.I)):
			HeaderDict[VINLen] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search('dsf.+seq',field,flags=re.I)):
			HeaderDict[DSF_WALK_SEQ] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bcrrt\b',field,flags=re.I)):
			HeaderDict[CRRT] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bzipcrrt\b',field,flags=re.I)):
			HeaderDict[ZipCRRT] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bkbb\b',field,flags=re.I)):
			HeaderDict[KBB] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bbuybackvalue\b',field,flags=re.I)):
			HeaderDict[BuybackValues] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bwinningnumber\b',field,flags=re.I)):
			HeaderDict[WinningNum] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bmaildnq\b',field,flags=re.I)):
			HeaderDict[MailDNQ] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bblitzdnq\b',field,flags=re.I)):
			HeaderDict[BlitzDNQ] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bdrop\b',field,flags=re.I)):
			HeaderDict[Drop] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bpurl\b',field,flags=re.I)):
			HeaderDict[PURL] = 'line[{}]'.format(str(OldColumn)) 
		elif bool(re.search(r'\byrdec\b',field,flags=re.I)):
			HeaderDict[YrDec] = 'line[{}]'.format(str(OldColumn))		
		elif bool(re.search(r'\bscf3dfacility\b',field,flags=re.I)):
			HeaderDict[SCF3DFacility] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bvendor\b',field,flags=re.I)):
			HeaderDict[Vendor] = 'line[{}]'.format(str(OldColumn))
		elif bool(re.search(r'\bmisc1\b',field,flags=re.I)):
			HeaderDict[Misc1] = 'line[{}]'.format(str(OldColumn)) 
		elif bool(re.search(r'\bmisc2\b',field,flags=re.I)):
			HeaderDict[Misc2] = 'line[{}]'.format(str(OldColumn)) 
		elif bool(re.search(r'\bmisc3\b',field,flags=re.I)):
			HeaderDict[Misc3] = 'line[{}]'.format(str(OldColumn))

	for index in tqdm(range(0,len(CSVFiles))):
		global OldColumn
		global NewColumn
		with open(CSVFiles[index],'rU') as InputFile,\
		open('___ReMapped--' + str(CSVFiles[index]),'at') as OutputFile:
			Input = csv.reader(InputFile)
			Output = csv.writer(OutputFile)
			Output.writerow(HeaderRowMain)
			FirstLine = True
			for line in tqdm(Input):
				if FirstLine:	
					for OldColumn in range(0,len(line)):
						match(line[OldColumn])
					FirstLine = False
				else:
					Newline = []
					for NewColumn in range(0,len(HeaderRowMain)):
						if NewColumn in HeaderDict:
							Newline.append(eval(HeaderDict[NewColumn]))
						else:
							Newline.append('')
					Output.writerow(Newline)

def MultiFileMarge():
	FirstFileUseHeaderRow = True
	CSVFiles = glob.glob('___*.csv')
	for line in tqdm(CSVFiles):
		with open(line,'rU') as File,\
		open('>>>> MERGED_FILE <<<<.csv','at') as Merge:
			OutputClean = csv.writer(Merge)
			Input = csv.reader(File)
			if FirstFileUseHeaderRow:
				for line in tqdm(Input):
					OutputClean.writerow(line)
				FirstFileUseHeaderRow = False
			else:
				next(File)
				for line in tqdm(Input):
					OutputClean.writerow(line)
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
	ReMapHeaderFields()
	MultiFileMarge()
