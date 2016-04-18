
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import re, os, glob
import pandas as pd
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
# ---------------------------------------------------------------------------- #
def ConvertXLStoCSV():
  XLSFiles = glob.glob('*.xls')
  for file in tqdm(XLSFiles):
    df = pd.read_excel(file)
    df.to_csv('{}.csv'.format(file.strip('.xls')),index=False)
# ---------------------------------------------------------------------------- #
def ConvertXLSXtoCSV():
  XLSXFiles = glob.glob('*.xlsx')
  for file in tqdm(XLSXFiles):
    df = pd.read_excel(file)
    df.to_csv('{}.csv'.format(file.strip('.xlsx')),index=False)
# ---------------------------------------------------------------------------- #
def Upkeep():
  Files = glob.glob('*.xls')
  for Record in Files:
    if bool(re.match('.+.xls',Record,flags=re.I)):
      os.remove(Record)
  Files = glob.glob('*.xlsx')
  for Record in Files:
    if bool(re.match('.+.xlsx',Record,flags=re.I)):
      os.remove(Record)
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
  print('=======================================')
  print('           CONVERT XLS to CSV          ')
  print('=======================================')
  ConvertXLStoCSV()
  ConvertXLSXtoCSV()
  Upkeep()
  print('=======================================')
  print('               COMPLETED               ')
  print()
