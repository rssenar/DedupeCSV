#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import os
import pandas as pd

os.chdir('../../../../Desktop/')

df = pd.read_csv('CHAPMAN CJ HENDERSON.csv')
print(df.shape)