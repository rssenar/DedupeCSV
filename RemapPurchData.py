
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
HeaderDict = {}
# ---------------------------------------------
def match(field):
	if bool(re.search('cus.+id',field,flags=re.I)):
		HeaderDict[0] = 'line['+str(i)+']'
	elif bool(re.search('fir.+me',field,flags=re.I)):
		HeaderDict[1] = 'line['+str(i)+']'
	elif bool(re.search(r'\bmi\b',field,flags=re.I)) or\
		bool(re.search(r'\bmiddle\b',field,flags=re.I)):
		HeaderDict[2] = 'line['+str(i)+']' 
	elif bool(re.search('las.+me',field,flags=re.I)):
		HeaderDict[3] = 'line['+str(i)+']' 
	elif bool(re.search('.ddr.+1',field,flags=re.I)):
		HeaderDict[4] = 'line['+str(i)+']' 
	elif bool(re.search('.ddr.+2',field,flags=re.I)):
		HeaderDict[5] = 'line['+str(i)+']' 
	elif bool(re.search('.ddr.+',field,flags=re.I)):
		HeaderDict[6] = 'line['+str(i)+']' 
	elif bool(re.search('.ity+',field,flags=re.I)):
		HeaderDict[7] = 'line['+str(i)+']' 
	elif bool(re.search('.tate',field,flags=re.I)):
		HeaderDict[8] = 'line['+str(i)+']' 
	elif bool(re.match(r'\bzip\b',field,flags=re.I)):
		HeaderDict[9] = 'line['+str(i)+']' 
	elif bool(re.search('4Z.+',field,flags=re.I)):
		HeaderDict[10] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bscf\b',field,flags=re.I)):
		HeaderDict[11] = 'line['+str(i)+']' 
	elif bool(re.search('phon.+',field,flags=re.I)) or\
		bool(re.search(r'\bhph\b',field,flags=re.I)):
		HeaderDict[12] = 'line['+str(i)+']' 
	elif bool(re.search('.mail',field,flags=re.I)):
		HeaderDict[13] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bvin\b',field,flags=re.I)):
		HeaderDict[14] = 'line['+str(i)+']' 
	elif bool(re.search(r'\byear\b',field,flags=re.I)) or\
		bool(re.search(r'\bvyr\b',field,flags=re.I)):
		HeaderDict[15] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bmake\b',field,flags=re.I)) or\
		bool(re.search(r'\bvmk\b',field,flags=re.I)):
		HeaderDict[16] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bmodel\b',field,flags=re.I)) or\
		bool(re.search(r'\bvmd\b',field,flags=re.I)):
		HeaderDict[17] = 'line['+str(i)+']' 
	elif bool(re.search('de.+ate',field,flags=re.I)):
		HeaderDict[18] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bdate\b',field,flags=re.I)):
		HeaderDict[19] = 'line['+str(i)+']' 
	elif bool(re.search('.adi.+',field,flags=re.I)):
		HeaderDict[20] = 'line['+str(i)+']' 
	elif bool(re.search('coor.+',field,flags=re.I)):
		HeaderDict[21] = 'line['+str(i)+']' 
	elif bool(re.search('v.+len',field,flags=re.I)):
		HeaderDict[22] = 'line['+str(i)+']' 
	elif bool(re.search('dsf.+seq',field,flags=re.I)):
		HeaderDict[23] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bcrrt\b',field,flags=re.I)):
		HeaderDict[24] = 'line['+str(i)+']' 
	elif bool(re.search('zip.+rt',field,flags=re.I)):
		HeaderDict[25] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bkbb\b',field,flags=re.I)):
		HeaderDict[26] = 'line['+str(i)+']' 
	elif bool(re.search('buy.+val.+',field,flags=re.I)):
		HeaderDict[27] = 'line['+str(i)+']' 
	elif bool(re.search('winn.+er',field,flags=re.I)):
		HeaderDict[28] = 'line['+str(i)+']' 
	elif bool(re.search('mai.+DNQ',field,flags=re.I)):
		HeaderDict[29] = 'line['+str(i)+']' 
	elif bool(re.search('bli.+DNQ',field,flags=re.I)):
		HeaderDict[30] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bdrop\b',field,flags=re.I)):
		HeaderDict[31] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bmisc1\b',field,flags=re.I)):
		HeaderDict[32] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bmisc2\b',field,flags=re.I)):
		HeaderDict[33] = 'line['+str(i)+']' 
	elif bool(re.search(r'\bmisc3\b',field,flags=re.I)):
		HeaderDict[34] = 'line['+str(i)+']'

def matchoutput():
	global i
	global x
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
# ---------------------------------------------
for index in range(0,len(CSVFiles)):
	InputFile = open(CSVFiles[index],'rU')
	Input = csv.reader(InputFile)
	# ---------------------------------------------
	OutputFile = open('_ReMapped_' + str(CSVFiles[index]),'ab')
	Output = csv.writer(OutputFile)
	Output.writerow(HeaderRow)
	# ---------------------------------------------
	matchoutput()
# ---------------------------------------------
OutputFile.close()
InputFile.close()
# ---------------------------------------------



