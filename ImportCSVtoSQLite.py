
#!/usr/bin/env python3.4
# ---------------------------------------------
import pandas as pd
import sqlite3
from pandas.io import sql
import subprocess
# ---------------------------------------------
os.chdir('../../../../Desktop/')
CSVFiles = glob.glob('*.csv')
# ---------------------------------------------
input_csv = 'large.csv'
output_sqlite = 'my.sqlite'
# ---------------------------------------------
table_name = 'new_table' # name for the SQLite database table
itersize = 100000 # number of lines to process at each iteration
# ---------------------------------------------
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
# ---------------------------------------------
NumOfLines = subprocess.check_output(['wc','-l',input_csv])
NumOfLines = int(NumOfLines.split()[0]) 
# ---------------------------------------------
ConSQLiteDB = sqlite3.connect(output_sqlite)
# ---------------------------------------------
for file in tqdm(CSVFiles):
    for i in range(0, NumOfLines, itersize): # change 0 -> 1 if your csv contains header
        DataFrame = pd.read_csv(
            file,
            header = None,
            nrows = itersize,
            skiprows = i
            )
        DataFrame.columns = columns # columns to read
        sql.to_sql(
            DataFrame,
            name = table_name,
            con = ConSQLiteDB,
            index = False, # don't use CSV file index
            index_label = 'CustomerID', # use a unique column from DataFrame as index
            if_exists = 'append'
            )
    ConSQLiteDB.close()

if __name__ == '__main__':
    CSVtoSQLiteImport()