
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import csv, os, glob
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------------------------------------- #
def MultiFileMarge():
  FirstFileUseHeaderRow = True
  CSVFiles = glob.glob('*.csv')
  for line in tqdm(CSVFiles):
    with open(line,'rU') as File,\
    open('_MERGED_File.csv','at') as Merge:
      Input = csv.reader(File)
      OutputClean = csv.writer(Merge)
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
  MultiFileMarge()
