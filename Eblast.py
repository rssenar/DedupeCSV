#!/usr/bin/env python
from __future__ import division, print_function
import csv, os, glob, requests
from tqdm import tqdm
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
FirstTime = True
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------
HeaderRow = [\
	'PURL',\
	'First Name',\
	'Last Name',\
	'Address',\
	'City',\
	'State',\
	'Zip',\
	]
# ---------------------------------------------
for FileName in CSVFiles:
	InputFile = open(FileName,'rU')
	Input = csv.reader(InputFile)
# ---------------------------------------------
OutputFile = open('_EBLAST.csv','ab')
Output = csv.writer(OutputFile)
Output.writerow(HeaderRow)
# ---------------------------------------------
FirstLine = True
for line in tqdm(Input):
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		if FirstTime is True:
			PURL = line[0]
			PURL = 'http://' + PURL
			F_PURL = requests.get(PURL)
			F_PURL = str(F_PURL.url) + '8'
			FName = line[1] + line[2]
			x = F_PURL.split(FName)
			HeaderURL = x[0]
			FooterURL = x[1]
			New_PURL = HeaderURL + FName + FooterURL
			Output.writerow((\
				New_PURL,\
				line[1],\
				line[2],\
				line[3],\
				line[4],\
				line[5],\
				line[6]\
				))
			FirstTime = False
		else:
			FName = line[1] + line[2]
			New_PURL = HeaderURL + FName + FooterURL
			Output.writerow((\
				New_PURL,\
				line[1],\
				line[2],\
				line[3],\
				line[4],\
				line[5],\
				line[6]\
				))

OutputFile.close()
InputFile.close()
