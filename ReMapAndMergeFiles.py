
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import csv, os, glob
from Constants import *
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------------------------------------- #
# Re-Map Column Fields
def ReMapHeaderFields():
  for index in tqdm(range(0,len(CSVFiles))):
    with open(CSVFiles[index],'rU') as InputFile,\
    open('___ReMapped--' + str(CSVFiles[index]),'at') as OutputFile:
      Input = csv.reader(InputFile)
      Output = csv.writer(OutputFile)
      Output.writerow(HeaderRowMain)
      FirstLine = True
      for line in tqdm(Input):
        if FirstLine:
          for IndexA in range(0,len(line)):
            MatchHeaderFields(line[IndexA], IndexA)
          FirstLine = False
        else:
          Newline = []
          for IndexB in range(0,len(HeaderRowMain)):
            if IndexB in HeaderDict:
              Newline.append(eval(HeaderDict[IndexB]))
            else:
              Newline.append('')
          Output.writerow(Newline)

def MultiFileMarge():
  FirstFileUseHeaderRow = True
  CSVFiles = glob.glob('___*.csv')
  for line in tqdm(CSVFiles):
    with open(line,'rU') as File,\
    open('>>>> MERGED_FILE <<<<.csv','at') as Merge:
      OutputClean = csv.writer(Merge)
      Input = csv.reader(File)
      if FirstFileUseHeaderRow:
        for line in tqdm(Input):
          OutputClean.writerow(line)
        FirstFileUseHeaderRow = False
      else:
        next(File)
        for line in tqdm(Input):
          OutputClean.writerow(line)
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
  print('=======================================')
  print('             RE-MAP & MERGE            ')
  print('=======================================')
  ReMapHeaderFields()
  MultiFileMarge()
  print('=======================================')
  print('               COMPLETED               ')
  print()
