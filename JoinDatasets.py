
#!/usr/bin/env python3.4
# ---------------------------------------------
import os, csv, glob, re
import pandas as pd
from tqdm import tqdm
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
Seq = 0
ziproute = 1
Description = 2
Records = 3
total = 4
dfo = 5
Percentage = 6
RTotal = 7
AdjRec = 8
RecRTotal = 9

OutputHeaderRow = [
	'Seq',
	'ziproute',
	'Description',
	'Records',
	'total',
	'dfo',
	'Percentage',
	'RTotal',
	'AdjRec',
	'RecRTotal'
	]

def perc(part, whole):
	if whole == 0:
		return 0
	else:
		return 100 * float(part)/float(whole)

def Join():
	ds1 = pd.read_csv('a.csv')
	ds2 = pd.read_csv('b.csv')
	# ---------------------------------------------
	merged = ds1.merge(ds2, how='inner')
	merged['Percentage'] = ''
	merged['RTotal'] = '' 
	merged['AdjRec'] = '' 
	merged['AdjRecRTotal'] = '' 
	merged.to_csv('temp.csv', encoding='utf-8')
	
def ReformatOutputReport():
	CSVFiles = glob.glob('temp.csv')
	for File in tqdm(CSVFiles):
		with open(File,'rU') as InputFile,\
		open('REFINED DATA_.csv','at') as OutputFile:
			Input = csv.reader(InputFile)
			Output = csv.writer(OutputFile)
			Output.writerow(OutputHeaderRow)
			RunningTotal = 0
			AdjRecRTotal = 0
			next(InputFile)
			for row in tqdm(Input):
				if int(row[Records]) >= 135: 
					row[Percentage] = round(perc(row[Records],row[total]),0)
					RunningTotal += int(row[Records])
					row[RTotal] = RunningTotal
					if int(row[Percentage]) >= 74:
						row[AdjRec] = round(float(row[total]) * 0.73,0)
					else:
						row[AdjRec] = row[Records]
					AdjRecRTotal += int(row[AdjRec])
					row[RecRTotal] = AdjRecRTotal
					Output.writerow(row)

if __name__ == '__main__':
	Join()
	ReformatOutputReport()
	Files = glob.glob('*.csv')
	for Record in Files:
		if bool(re.match(r'\btemp\b', Record, flags = re.I)):
			os.remove(Record)

