
#!/usr/bin/env python3.4
# ---------------------------------------------------------------------------- #
import csv, os
# ---------------------------------------------------------------------------- #
def Validate():
  Message1 = 'Files Validated!'
  Message2 = '''
  $$$$$$$$\
  $$ |      $$$$$$\  $$$$$$\  $$$$$$\  $$$$$$\
  $$$$$\   $$  __$$\$$  __$$\$$  __$$\$$  __$$\
  $$  __|  $$ |  \__$$ |  \__$$ /  $$ $$ |  \__|
  $$$$$$$$\$$ |     $$ |     \$$$$$$  $$ |
  \________\__|     \__|      \______/\__|
  '''
  os.chdir('../../../../Desktop/')
  Entries = set()
  File1 = str.lower(input('Enter File 1 : '))
  File2 = str.lower(input('Enter File 2 : '))
  File3 = str.lower(input('Enter File 3 : '))
  InputFile = '{}.csv'.format(File1)
  DatabaseFile = '{}.csv'.format(File2)
  PurchaseFile = '{}.csv'.format(File3)
  # ------------------------------------------------------------------------ #
  if File2 != '':
    with open(DatabaseFile,'rU') as DatabaseFile:
      Database = csv.reader(DatabaseFile)
      next(DatabaseFile)
      for line in Database:
        Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))
      Purchase = csv.reader(PurchaseFile)

  if File3 != '':
    with open(PurchaseFile,'rU') as PurchaseFile:
      Purchase = csv.reader(PurchaseFile)
      next(PurchaseFile)
      for line in Purchase:
        Entries.add((line[1],line[2],line[3],line[4],line[5],line[6]))

  if File1 != '':
    ErrorCounter = 0
    with open(InputFile,'rU') as InputFile:
      Input = csv.reader(InputFile)
      next(InputFile)
      for line in Input:
        key = ((line[1],line[2],line[3],line[4],line[5],line[6]))
        if key not in Entries:
          with open("error.csv",'at') as ErrorFile:
            Error = csv.writer(ErrorFile)
            Error.writerow(line)
          ErrorCounter += 1

  if ErrorCounter > 0:
    print('{} Errors Found'.format(ErrorCounter))
    print(Message2)
  else:
    print(Message1)
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
  Validate()
