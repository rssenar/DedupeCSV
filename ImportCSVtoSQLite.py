
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import os, glob, sqlite3, subprocess, Constants
import pandas as pd
from pandas.io import sql
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------------------------------------- #
table_name = 'Premierworks' # name table
itersize = 100000 # number of lines to process at each iteration
# ---------------------------------------------------------------------------- #
def CSVtoSQLiteImport():
  for file in CSVFiles:
    CSVLineCount = subprocess.check_output(['wc','-l',file])
    CSVLineCount = int(CSVLineCount.split()[0])
    filename = file.strip('.csv')
    ConSQLiteDB = sqlite3.connect('{}_SQLite3.db'.format(filename))
    for row in tqdm(range(1,CSVLineCount,itersize)):
      DataFrame = pd.read_csv(
        file,
        header = None,
        nrows = itersize,
        skiprows = row,
        low_memory = False
        )
      DataFrame.columns = Constants.HeaderRowMain
      sql.to_sql(
        DataFrame,
        name = table_name,
        con = ConSQLiteDB,
        index = False,
        index_label = 'CustomerID',
        if_exists = 'append'
        )
    ConSQLiteDB.close()

if __name__ == '__main__':
  CSVtoSQLiteImport()
