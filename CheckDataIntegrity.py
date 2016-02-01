# ---------------------------------------------
#!/usr/bin/python2.7.10
# ---------------------------------------------
from __future__ import division, print_function
import csv
import pandas as pd
from tqdm import tqdm
# ---------------------------------------------
CSVFilesHaveHeaderRow = True
# ---------------------------------------------
InputFileName = raw_input("Input File Name : ")
InputFile = "../../../../Desktop/" + InputFileName + ".csv"
DatabaseFileName = raw_input("Database File : ")
DatabaseFile = "../../../../Desktop/" + DatabaseFileName + ".csv"
PurchaseFileName = raw_input("Purchase File : ")
PurchaseFile = "../../../../Desktop/" + PurchaseFileName + ".csv"
# ---------------------------------------------
Entries = set()
# ---------------------------------------------
InputFileDF = pd.read_csv(InputFile)
TotalRows = len(InputFileDF)
# ---------------------------------------------
InputFile = open(InputFile,'rb')
DatabaseFile = open(DatabaseFile,'rb')
PurchaseFile = open(PurchaseFile,'rb')
# ---------------------------------------------
Input = csv.reader(InputFile)
Database = csv.reader(DatabaseFile)
Purchase = csv.reader(PurchaseFile)
# ---------------------------------------------
FirstLine = True
for line in Database:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))
# ---------------------------------------------
FirstLine = True
for line in Purchase:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))
# ---------------------------------------------
Counter = 0
FirstLine = True
for line in tqdm(Input):
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		key = ((line[1],line[2],line[3],line[4],line[5],line[6]))
		if key in Entries:
			Counter += 1
Percentage = Counter / TotalRows * 100

if Percentage == 100:
	print(str(Percentage) + "%" + " Matches - PERFECT!")
else:
	print(str(Percentage) + "%" + " Matches - WE HAVE A PROBLEM!")
# ---------------------------------------------
InputFile.close()
DatabaseFile.close()
PurchaseFile.close()
# ---------------------------------------------