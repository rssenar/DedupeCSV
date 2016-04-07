
#!/usr/bin/env python3.4
# ---------------------------------------------
import os, csv, glob, re
import pandas as pd
from tqdm import tqdm
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
Seq = 1
ziproute = 2
Description = 3
Records = 4
total = 5
dfo = 6
Percentage = 7
RTotal = 8

OutputHeaderRow = [
	'Seq1',
	'Seq2',
	'ziproute',
	'Description',
	'Records',
	'total',
	'dfo',
	'Percentage',
	'RTotal',
	]

def perc(part, whole):
	if whole == 0:
		return 0
	else:
		return 100 * float(part)/float(whole)

def Join():
	#File1 = input('Enter 1st Dataset: ')
	#FileName1 = '{}.csv'.format(File1)
	#File2 = input('Enter 2nd Dataset: ')
	#FileName2 = '{}.csv'.format(File2)
	#ds1 = pd.read_csv(FileName1)
	#ds2 = pd.read_csv(FileName2)
	# ---------------------------------------------	
	ds1 = pd.read_csv('a.csv')
	ds2 = pd.read_csv('b.csv')
	# ---------------------------------------------
	merged = ds1.merge(ds2, how='inner')
	merged.to_csv('temp1.csv', encoding='utf-8')
	df = pd.read_csv('temp1.csv')
	df['Percentage'] = ''
	df['RTotal'] = ''
	df.to_csv('temp2.csv')

def ReformatOutputReport():
	CSVFiles = glob.glob('temp2.csv')
	for File in tqdm(CSVFiles):
		with open(File,'rU') as InputFile, open('REFINED DATA_.csv','at') as OutputFile:
			Input = csv.reader(InputFile)
			Output = csv.writer(OutputFile)
			Output.writerow(OutputHeaderRow)
			RunningTotal = 0
			next(InputFile)
			for row in tqdm(Input):
				if int(row[Records]) >= 135: 
					row[Percentage] = round(perc(row[Records],row[total]),0)
					RunningTotal += int(row[Records])
					row[RTotal] = RunningTotal
					Output.writerow(row)

if __name__ == '__main__':
	Join()
	ReformatOutputReport()
	Files = glob.glob('*.csv')
	for Record in Files:
		if bool(re.match(r'\btemp1\b', Record, flags = re.I)):
			os.remove(Record)
		if bool(re.match(r'\btemp2\b', Record, flags = re.I)):
			os.remove(Record)