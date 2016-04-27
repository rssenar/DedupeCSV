
import os, csv, glob
# ------------------------------ #
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ------------------------------ #
CSVFiles = glob.glob('*.csv')
for line in CSVFiles:
  with open(line,'rU') as File:
    Input = csv.reader(File)
    for line in Input:
      if '-' in line[0]:
        pass
      else:
        line[0] = line[0].split(',')
        x = line[0][0][:3]
        for i in line[0]:
          i = i.strip()
          if len(i) == 5:
            print('{}, {}'.format(i,line[1]))
          else:
            print('{}{}, {}'.format(x,i,line[1]))

