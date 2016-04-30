
import os, csv, glob, re
# ------------------------------ #
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ------------------------------ #
CSVFiles = glob.glob('*.csv')
for line in CSVFiles:
  with open(line,'rU', encoding = "ISO-8859-1") as File:
    InputFile = csv.reader(File)
    for Row in InputFile:
      Row[0] = Row[0].split(',')
      for i in Row[0]:
        i = i.strip()
        if bool(re.search(r'\b[0-9][0-9][0-9]\b',i,flags=re.I)) and len(i) == 5:
          print('{}, {}'.format(i, Row[1]))
        elif bool(re.search(r'\b[0-9][0-9][0-9]-[0-9][0-9][0-9]\b',i,flags=re.I)):
          i = i.split('-')
          for z in range(int(i[0]),int(i[1])+1):
            print('{}, {}'.format(str(z).zfill(3), Row[1]))
