
#!/usr/bin/env python3.4
# ---------------------------------------------
import os
import pandas as pd
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
def PDJoin():
	File1 = raw_input('Enter 1st Dataset: ')
	FileName1 = '{}.csv'.format(File1)
	File2 = raw_input('Enter 2nd Dataset: ')
	FileName2 = '{}.csv'.format(File2)
	# ---------------------------------------------
	ds1 = pd.read_csv(FileName1)
	ds2 = pd.read_csv(FileName2)
	# ---------------------------------------------
	merged = ds1.merge(ds2, how='inner')
	merged.to_csv('__JOINED.csv', encoding='utf-8')

if __name__ == '__main__':
	PDJoin()