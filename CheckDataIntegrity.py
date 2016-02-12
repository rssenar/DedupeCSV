#!/usr/bin/env python
from __future__ import division, print_function
import csv, os
import pandas as pd
from tqdm import tqdm
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
# ---------------------------------------------
os.chdir('../../../../Desktop/')
Entries = set()
# ---------------------------------------------
# InputFile = raw_input("Input File Name : ") + ".csv"
# DatabaseFile = raw_input("Database File : ") + ".csv"
# PurchaseFile = raw_input("Purchase File : ") + ".csv"
InputFile = "a.csv"
DatabaseFile = "b.csv"
PurchaseFile = "c.csv"
# ---------------------------------------------
InputFileDF = pd.read_csv(InputFile)
TotalRows = len(InputFileDF)
# ---------------------------------------------
DatabaseFile = open(DatabaseFile,'rU')
Database = csv.reader(DatabaseFile)
FirstLine = True
for line in Database:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))
DatabaseFile.close()
# ---------------------------------------------
PurchaseFile = open(PurchaseFile,'rU')
Purchase = csv.reader(PurchaseFile)
FirstLine = True
for line in Purchase:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))
PurchaseFile.close()
# ---------------------------------------------
InputFile = open(InputFile,'rU')
Input = csv.reader(InputFile)
Counter = 0
FirstLine = True
for line in tqdm(Input):
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		key = ((line[1],line[2],line[3],line[4],line[5],line[6]))
		if key in Entries:
			Counter += 1
		else:
			ErrorFile = open("error.csv",'ab')
			Error = csv.writer(ErrorFile)
			Error.writerow(line)
			ErrorFile.close()
InputFile.close()
# ---------------------------------------------
Percentage = Counter/TotalRows*100
if Percentage == 100:
	print(str(Percentage) + "%" + " Matches - OK!")
else:
	print(str(Percentage) + "%" + " Matches - !!WARNING!! -- !!WARNING!! -- !!WARNING!!")
