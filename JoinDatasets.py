#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import pandas as pd
import os
# ---------------------------------------------
os.chdir('../../../../Desktop/')
# ---------------------------------------------
File1 = raw_input('Enter 1st Dataset: ')
FileName1 = '{}.csv'.format(File1)
File2 = raw_input('Enter 2nd Dataset: ')
FileName2 = '{}.csv'.format(File2)
# ---------------------------------------------
ds1 = pd.read_csv(FileName1)
ds2 = pd.read_csv(FileName2)
# ---------------------------------------------
merged = ds1.merge(ds2, how='inner')
merged.to_csv('__Joined.csv', encoding='utf-8')