#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, glob, requests
from tqdm import tqdm
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
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
def PURLConversion():
	global FirstTime
	global FirstLine
	global HeaderURL
	global FooterURL
	for line in tqdm(Input):
		if CSVFilesHaveHeaderRow and FirstLine:
			FirstLine = False
		else:
			if FirstTime is True:
				PURL = 'http://' + line[0]
				F_PURL = requests.get(PURL)
				F_PURL = str(F_PURL.url) + '8'
				FName = line[1] + line[2]
				URL = F_PURL.split(FName)
				HeaderURL = URL[0]
				FooterURL = URL[1]
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
# ---------------------------------------------
for index in range(0,len(CSVFiles)):
	FirstTime = True
	FirstLine = True
	InputFile = open(CSVFiles[index],'rU')
	Input = csv.reader(InputFile)
	OutputFile = open('_Eblast_' + str(CSVFiles[index]),'ab')
	Output = csv.writer(OutputFile)
	Output.writerow(HeaderRow)
	PURLConversion()
# ---------------------------------------------
OutputFile.close()
InputFile.close()
# ---------------------------------------------