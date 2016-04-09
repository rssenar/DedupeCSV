
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import os, glob, sqlite3, subprocess
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
columns = [
    'CustomerID',
    'FullName',
    'FirstName',
    'MI',
    'LastName',
    'Address1',
    'Address2',
    'AddressFull',
    'City',
    'State',
    'Zip',
    '4Zip',
    'SCF',
    'Phone',
    'HPH',
    'BPH',
    'CPH',
    'Email',
    'VIN',
    'Year',
    'Make',
    'Model',
    'DelDate',
    'Date',
    'Radius',
    'Coordinates',
    'VINLen',
    'DSF_WALK_SEQ',
    'Crrt',
    'ZipCrrt',
    'KBB',
    'BuybackValue',
    'WinningNumber',
    'MailDNQ',
    'BlitzDNQ',
    'Drop',
    'PURL',
    'YrDec',
    'SCF3DFacility',
    'Vendor',
    'Misc1',
    'Misc2',
    'Misc3'
    ]
# ---------------------------------------------------------------------------- #
def CSVtoSQLiteImport():
    for file in tqdm(CSVFiles):
        CSVLineCount = subprocess.check_output(['wc','-l',file]) # CSV line count
        CSVLineCount = int(CSVLineCount.split()[0]) # extract count value
        filename = file.strip('.csv') # strip .csv from filename
        ConSQLiteDB = sqlite3.connect('{}_SQLite3.db'.format(filename))
        for row in tqdm(range(1,CSVLineCount,itersize)): #skip header row
            DataFrame = pd.read_csv(
                file,
                header = None,
                nrows = itersize,
                skiprows = row,
                low_memory = False
                )
            DataFrame.columns = columns
            sql.to_sql(
                DataFrame,
                name = table_name,
                con = ConSQLiteDB,
                index = False,
                index_label = 'CustomerID',
                if_exists = 'append'
                )
        ConSQLiteDB.close()
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    CSVtoSQLiteImport()
