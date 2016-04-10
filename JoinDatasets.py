
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import os, csv, glob, re
import pandas as pd
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
# ---------------------------------------------------------------------------- #
File1 = 'a.csv'
File2 = 'b.csv'

ziproute = 0
Description = 1
Records = 2
total = 3
dfo = 4
Percentage = 5
RTotal = 6
AdjRec = 7
AdjRecPerc = 8
RecRTotal = 9

OutputHeaderRow = [
	'ziproute',
	'Description',
	'Records',
	'Total_Sat',
	'Dist(m)',
	'Sat%',
	'R-TOTAL',
	'ADJ_Rec',
	'ADJ_Sat%',
	'ADJ_R-TOTAL'
	]

def Perc(part, whole):
	if whole == 0:
		return 0
	else:
		return 100 * float(part)/float(whole)

def Join():
	ds1 = pd.read_csv(File1)
	ds2 = pd.read_csv(File2)
	merged = ds1.merge(ds2, how = 'inner')
	merged['Percentage'] = ''
	merged['RTotal'] = '' 
	merged['AdjRec'] = ''
	merged['AdjRecPerc'] = '' 
	merged['AdjRecRTotal'] = '' 
	merged.to_csv('temp.csv', encoding = 'utf-8', index=False)
	
def ReformatOutputReport():
	CSVFiles = glob.glob('temp.csv')
	for file in tqdm(CSVFiles):
		with open(file,'rU') as InputFile,\
		open('DATA.csv','at') as OutputFile:
			Input = csv.reader(InputFile)
			Output = csv.writer(OutputFile)
			Output.writerow(OutputHeaderRow)
			RunningTotal = 0
			AdjRecRTotal = 0
			RowCounter = 2
			next(InputFile)
			for Row in tqdm(Input):
				if int(Row[Records]) >= 135: 
					Row[dfo] = round(float(Row[dfo]),1)
					Row[Percentage] = round(Perc(Row[Records],Row[total]),0)
					Row[RTotal] = '=SUM($D$2:$D{})'.format(RowCounter)
					if int(Row[Percentage]) >= 74:
						Row[AdjRec] = round(float(Row[total]) * 0.73,0)
					else:
						Row[AdjRec] = Row[Records]
					Row[AdjRecPerc] = round(Perc(Row[AdjRec],Row[total]),0)
					Row[RecRTotal] = '=SUM($I$2:$I{})'.format(RowCounter)
					Output.writerow(Row)
					RowCounter += 1
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
	Join()
	ReformatOutputReport()
	Files = glob.glob('*.csv')
	for Record in Files:
		if bool(re.match(r'\btemp\b', Record, flags = re.I)):
			os.remove(Record)

