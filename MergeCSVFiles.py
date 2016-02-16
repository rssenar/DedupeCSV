#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, glob
from tqdm import tqdm
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
FirstFileUseHeaderRow = True
# ---------------------------------------------
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------
Merge = open('_MergeFile.csv','ab')
OutputClean = csv.writer(Merge)
# ---------------------------------------------
for line in CSVFiles:
	File = open(line,'rU')
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
Merge.close()
File.close()
# ---------------------------------------------