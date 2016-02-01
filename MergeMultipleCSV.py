#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, glob
from tqdm import tqdm
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
FirstFileUseHeaderRow = True
# ---------------------------------------------
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
OutputClean = csv.writer(open('__MergeFile.csv','ab'))
# ---------------------------------------------
for line in CSVFiles:
	Input = csv.reader(open(line,'rU'))
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
