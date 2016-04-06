
#!/usr/bin/env python3.4
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
def MultiFileMarge():
	CSVFilesHaveHeaderRow = True
	FirstFileUseHeaderRow = True
	CSVFiles = glob.glob('*.csv')
	for line in CSVFiles:
		with open(line,'rU') as File, open('___MergedFile.csv','ab') as Merge:
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
MultiFileMarge()
# ---------------------------------------------


