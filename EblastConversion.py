
#!/usr/bin/env python3.4
# ---------------------------------------------
import csv, os, glob, requests
from tqdm import tqdm
# ---------------------------------------------
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------
Website = 0
FirstName = 1
LastName = 2
Address = 3
City = 4
State = 5
Zip = 6
HeaderRow = [
	'PURL',
	'First Name',
	'Last Name',
	'Address',
	'City',
	'State',
	'Zip'
	]
# ---------------------------------------------
def PURLConversion():
	global FirstTime
	for line in tqdm(Input):
		if FirstTime:
			PURL = '{}{}'.format(
				'http://',
				line[Website]
				)
			F_PURL = requests.get(PURL)
			F_PURL = '{}{}'.format(
				str(F_PURL.url),
				'8'
				)
			FirstLastName = '{}{}'.format(
				line[FirstName],
				line[LastName]
				)
			URL = F_PURL.split(FirstLastName)
			HeaderURL = URL[Website]
			FooterURL = URL[FirstName]
			New_PURL = '{}{}{}'.format(
				HeaderURL,
				FirstLastName,
				FooterURL
				)
			Output.writerow((
				New_PURL,
				line[FirstName],
				line[LastName],
				line[Address],
				line[City],
				line[State],
				line[Zip]
				))
			FirstTime = False
		else:
			FirstLastName = '{}{}'.format(
				line[FirstName],
				line[LastName]
				)
			New_PURL = '{}{}{}'.format(
				HeaderURL,
				FirstLastName,
				FooterURL
				)
			Output.writerow((
				New_PURL,
				line[FirstName],
				line[LastName],
				line[Address],
				line[City],
				line[State],
				line[Zip]
				))
# ---------------------------------------------
if __name__ == '__main__':
	for index in range(0,len(CSVFiles)):
	FirstTime = True
	with open(CSVFiles[index],'rU') as InputFile,\
	open('EBLAST_' + str(CSVFiles[index]),'at') as OutputFile:
		Input = csv.reader(InputFile)
		next(InputFile) # skip header row
		Output = csv.writer(OutputFile)
		Output.writerow(HeaderRow)
		PURLConversion()
