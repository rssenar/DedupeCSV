#!/usr/bin/env python
from __future__ import division, print_function
import csv, os, glob
from tqdm import tqdm
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
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
# ---------------------------------------------
OutputFile = open('_ReMappedFile.csv','ab')
Output = csv.writer(OutputFile)
Output.writerow(HeaderRow)
# ---------------------------------------------
for FileName in CSVFiles:
	InputFile = open(FileName,'rU')
	Input = csv.reader(InputFile)

FirstLine = True
for line in tqdm(Input):
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		Output.writerow((\
			'',\
			line[2],\
			'',\
			line[4],\
			line[5],\
			line[6],\
			'',\
			line[7],\
			line[8],\
			line[9],\
			line[10],\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			line[18],\
			line[12],\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			'',\
			''\
			))
# ---------------------------------------------
OutputFile.close()
InputFile.close()
# ---------------------------------------------
