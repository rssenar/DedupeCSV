
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import csv, os, subprocess
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
def percentage(part, whole):
	if whole == 0:
		return 0
	else:
		return 100 * float(part)/float(whole)

def Validate():
	Message1 = 'Files Validated!'
	Message2 = '''
	$$$$$$$$\                                     
	$$ |      $$$$$$\  $$$$$$\  $$$$$$\  $$$$$$\  
	$$$$$\   $$  __$$\$$  __$$\$$  __$$\$$  __$$\ 
	$$  __|  $$ |  \__$$ |  \__$$ /  $$ $$ |  \__|
	$$$$$$$$\$$ |     $$ |     \$$$$$$  $$ |      
	\________\__|     \__|      \______/\__|      
	'''
	os.chdir('../../../../Desktop/')
	Entries = set()
	File1 = str.lower(input('Enter File 1 : '))
	File2 = str.lower(input('Enter File 2 : '))
	File3 = str.lower(input('Enter File 3 : '))
	InputFile = '{}.csv'.format(File1)
	DatabaseFile = '{}.csv'.format(File2)
	PurchaseFile = '{}.csv'.format(File3)
	# ------------------------------------------------------------------------ #
	CSVLineCount = subprocess.check_output(['wc','-l',InputFile])
	CSVLineCount = int(CSVLineCount.split()[0])
	# ------------------------------------------------------------------------ #
	if File2 != '':
		with open(DatabaseFile,'rU') as DatabaseFile:
			Database = csv.reader(DatabaseFile)
			next(DatabaseFile)
			for line in Database:
				Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))
			Purchase = csv.reader(PurchaseFile)

	if File3 != '':
		with open(PurchaseFile,'rU') as PurchaseFile:
			Purchase = csv.reader(PurchaseFile)
			next(PurchaseFile)
			for line in Purchase:
				Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))

	if File1 != '':
		Counter = 0
		with open(InputFile,'rU') as InputFile:
			Input = csv.reader(InputFile)
			next(InputFile)
			for line in tqdm(Input):
				key = ((line[1],line[2],line[3],line[4],line[5],line[6]))
				if key in Entries:
					Counter+=1
				else:
					with open("error.csv",'at') as ErrorFile:
						Error = csv.writer(ErrorFile)
						Error.writerow(line)
	
	Percentage = round(percentage(Counter,CSVLineCount),1)
	if Percentage == 100:
		print('{}% {}'.format(Percentage,Message1))
	else:
		print('{}% {}'.format(Percentage,Message2))
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
	Validate()
