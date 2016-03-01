
#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import csv, os, glob
from tqdm import tqdm
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
def MultiFileMarge():
	CSVFilesHaveHeaderRow = True
	FirstFileUseHeaderRow = True
	CSVFiles = glob.glob('_*.csv')
	for line in CSVFiles:
		with open(line,'rU') as File, open('_MergeFile.csv','ab') as Merge:
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