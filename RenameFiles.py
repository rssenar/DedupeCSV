
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import os, glob, time
from dateutil.parser import *
from tqdm import tqdm
# ---------------------------------------------------------------------------- #
os.chdir('../../../../Desktop/')
print('=======================================')
print('          R E N A M E  F I L E         ')
print('=======================================')
NewName = input('Enter New Name ................ : ').strip()
FileType = input('Enter File Type (.jpg|.xls) ... : ').strip()
# ---------------------------------------------------------------------------- #
def RenameFiles():
	SeqNum = 1
	Files = glob.glob('*{}'.format(FileType))
	for Record in Files:
		FileDate = time.strftime('%Y-%d-%m', time.gmtime(os.path.getmtime(Record)))
		NewFileName = '{}_{}_{}{}'.format(NewName, FileDate, str(SeqNum).zfill(6), FileType)
		os.rename(Record, NewFileName)
		SeqNum += 1
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
	RenameFiles()
