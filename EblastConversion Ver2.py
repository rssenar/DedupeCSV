
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import csv, os, glob, requests, re
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------------------------------------- #
Website = 0
FirstName = 1
LastName = 2
Phone = 3
Address = 4
City = 5
State = 6
Zip = 7
Year = 8
Make = 9
Model = 10
TempEmail = 11

HeaderRow = [
  'PURL',
  'First Name',
  'Last Name',
  'Phone',
  'Address',
  'City',
  'State',
  'Zip',
  'Year',
  'Make',
  'Model',
  'TempEmail'
  ]
# ---------------------------------------------------------------------------- #
def PURLConversion():
  global FirstTime
  for line in tqdm(Input):
    if FirstTime:
      PURL = line[Website]
      if not bool(re.search(r'http://',PURL,flags=re.I)):
        PURL = '{}{}'.format(
          'http://',
          line[Website]
          )
      O_PURL = requests.get(PURL)
      F_PURL = '{}{}'.format(
        str(O_PURL.url),
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
        line[Phone],
        line[Address],
        line[City],
        line[State],
        line[Zip],
        line[Year],
        line[Make],
        line[Model],
        line[TempEmail]
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
        line[Phone],
        line[Address],
        line[City],
        line[State],
        line[Zip],
        line[Year],
        line[Make],
        line[Model],
        line[TempEmail]
        ))
  if O_PURL.status_code != requests.codes.ok:
    print('{}\nPage Not Found for {}'.format(ErrorMessage, CSVFiles[index]))
  else:
    print('{}\nEblast Conversion Completed for {}'.format(OKMessage, CSVFiles[index]))

ErrorMessage = '''
 /$$   /$$ /$$$$$$ /$$   /$$     /$$$$$$$$
| $$  | $| $$$$\ $| $$  | $$    | $$       /$$$$$$  /$$$$$$  /$$$$$$  /$$$$$$
| $$$$$$$| $$ $$ $| $$$$$$$$    | $$$$$   /$$__  $$/$$__  $$/$$__  $$/$$__  $$
|_____  $| $$\ $$$|_____  $$    | $$__/  | $$  \__| $$  \__| $$  \ $| $$  \__/
      | $|  $$$$$$/     | $$    | $$$$$$$| $$     | $$     |  $$$$$$| $$
      |__/\______/      |__/    |________|__/     |__/      \______/|__/
'''
OKMessage = '''
  /$$$$$$  /$$$$$$  /$$$$$$       /$$$$$$ /$$   /$$
 /$$__  $$/$$$_  $$/$$$_  $$     /$$__  $| $$  /$$/
  /$$$$$$| $$ $$ $| $$ $$ $$    | $$  | $| $$$$$/
| $$     | $$ \ $$| $$ \ $$$    | $$  | $| $$\  $$
| $$$$$$$|  $$$$$$|  $$$$$$/    |  $$$$$$| $$ \  $$
|________/\______/ \______/      \______/|__/  \__/
'''
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
  print('=======================================')
  print('           EBLAST CONVERSION           ')
  print('=======================================')
  for index in range(0,len(CSVFiles)):
    FirstTime = True
    with open(CSVFiles[index],'rU') as InputFile,\
    open('EBLAST_' + str(CSVFiles[index]),'at') as OutputFile:
      Input = csv.reader(InputFile)
      next(InputFile)
      Output = csv.writer(OutputFile)
      Output.writerow(HeaderRow)
      PURLConversion()
