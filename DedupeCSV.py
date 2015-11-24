'''                                                                                                                           
 +-+-+-+-+-+-+ +-+-+-+
 |D|e|d|u|p|e| |C|S|V|
 +-+-+-+-+-+-+ +-+-+-+  
'''
#!/usr/bin/python3.4.3
# Required Modules
import csv
# ---------------------------------------------
'''
 +-+-+-+-+-+-+-+-+-+
 |V|a|r|i|a|b|l|e|s|
 +-+-+-+-+-+-+-+-+-+
'''
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
# ---------------------------------------------
InputFile = "/Users/rssenar/Desktop/Tomball Ford DATABASE.csv" 
# ---------------------------------------------
CleanOutput = "/Users/rssenar/Desktop/_CleanOutput.csv"
Dupes = "/Users/rssenar/Desktop/_Dupes.csv" 
# ---------------------------------------------
'''
Select Criteria : 
OPHH = One Record Per House Hold
OPP = One Record Per Person
VIN = Vin#
'''
Selection = 'OPHH'
'''
+-+-+-+-+-+-+
|L|e|g|e|n|d|
+-+-+-+-+-+-+
'''
# Column[0] = CustomerID
# Column[1] = FirstName
# Column[2] = MI
# Column[3] = LastName
# Column[4] = Address1
# Column[5] = Address2
# Column[6] = AddressCombined
# Column[7] = City
# Column[8] = State
# Column[9] = Zip
# Column[10] = Zip + 4
# Column[11] = SCF
# Column[12] = Phone
# Column[13] = Email
# Column[14] = VIN
# Column[15] = TradeYear
# Column[16] = TradeMake
# Column[17] = TradeModel
# Column[18] = DelDate
# Column[19] = Date
# Column[20] = Radius
# Column[21] = Vin Number Length
# Column[22] = DSF_WALK_SEQ
# Column[23] = CRRT
# Column[24] = KBB
# Column[25] = Buyback Value
# Column[26] = Winning Number
# Column[27] = Misc1
# Column[28] = Misc2
# Column[29] = Misc3
# ---------------------------------------------
# Assign variables for readability
# ---------------------------------------------
FName = 1
LName = 3
Address1 = 4
Address2 = 5
AddressCombined = 6
City = 7
Zip = 9
SCF = 11
Email = 13
VIN = 14
TradeYear = 15
TradeMake = 16
TradeModel = 17
Radius = 20
VINLen = 21
WinningNum = 26
# ----------------------------------------------
Entries = set() # Alocate Entries set to emplty
# ----------------------------------------------
''' 
 +-+-+-+-+-+-+-+
 |O|b|j|e|c|t|s|
 +-+-+-+-+-+-+-+ 
'''
# ----------------------------------------------
Input = csv.reader(open(InputFile,'r')) # Read in the input file
OutputClean = csv.writer(open(CleanOutput,'a')) # Open Processed output file
OutDupes = csv.writer(open(Dupes,'a')) # Open Dupes file
# Append Header Row to Processed output file
OutputClean.writerow(['Customer ID','First Name','MI','Last Name','Address1','Address2','Address','City','State','Zip','4Zip','SCF',\
	'Phone','Email','VIN','TradeYear','TradeMake','TradeModel','DelDate','Date','Radius','VINLen','DSF_WALK_SEQ','Crrt','KBB','Buyback Value',\
	'Winning Number','Misc1','Misc2','Misc3'])
# Append Header Row to Dupes file
OutDupes.writerow(['Customer ID','First Name','MI','Last Name','Address1','Address2','Address','City','State','Zip','4Zip','SCF',\
	'Phone','Email','VIN','TradeYear','TradeMake','TradeModel','DelDate','Date','Radius','VINLen','DSF_WALK_SEQ','Crrt','KBB','Buyback Value',\
	'Winning Number','Misc1','Misc2','Misc3'])
# ----------------------------------------------
'''
 +-+-+-+-+-+-+-+-+-+
 |F|u|n|c|t|i|o|n|s|
 +-+-+-+-+-+-+-+-+-+
'''
# ----------------------------------------------
def SetCase(): # Set case fields
	line[FName] = str.title(line[FName]) 
	line[LName] = str.title(line[LName])
	line[Address1] = str.title(line[Address1])
	line[Address2] = str.title(line[Address2])
	line[City] = str.title(line[City])
	line[TradeYear] = str.title(line[TradeYear])
	line[TradeMake] = str.title(line[TradeMake])
	line[TradeModel] = str.title(line[TradeModel])
	line[Email] = str.lower(line[Email])

def SetRadiusToInteger():
	if line[Radius] == 'Null':
		line[Radius] = line[Radius]
	else:
		if line[Radius] == "":
			line[Radius] = 'Null'
		else:
			line[Radius] = int(float(line[Radius]))

def SetVINLen(): # Assign the Length of the VIN# to VinLen Field
	line[VINLen] = len(line[VIN])

def SetWinningNum(): # Assign Winning Number to Winning Number Field
	line[WinningNum] = 40754

def CombineAddress(): # Combine Address 1 & Address 2 fields
	if line[AddressCombined] == "":
		if line[Address2] == "":
			line[AddressCombined] = line[Address1] # If Address2 is empty
		else:
			line[AddressCombined] = line[Address1] + ' ' + line[Address2]
	else:
		line[AddressCombined] = str.title(line[AddressCombined])

def SetSCF(): # Parse VIN# then assign value to SCF field
	ZipLen = len(line[Zip])
	if ZipLen < 5:
		line[SCF] = (line[Zip])[:2] # if ZIP is less than 5 Digits, usually because leading 0 is dropped
	else:
		line[SCF] = (line[Zip])[:3] # if ZIP is 5 Digits

def CheckDupesAndOutput():
	if key not in Entries: # Check if key is in the Entries set
		OutputClean.writerow(line) # write to processed output file
		Entries.add(key) # add row to Entries set
	else:
		OutDupes.writerow(line) # write to Dupes file
# ----------------------------------------------
'''
 +-+-+-+-+ +-+-+-+-+-+-+-+
 |M|a|i|n| |P|r|o|g|r|a|m|
 +-+-+-+-+ +-+-+-+-+-+-+-+
'''
# ----------------------------------------------
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		SetCase()
		SetVINLen()
		SetWinningNum()
		SetSCF()
		CombineAddress()
		SetRadiusToInteger()
		if Selection == 'OPHH': # Checks Selection Criteria
			key = (line[AddressCombined],line[Zip])
			CheckDupesAndOutput()
		elif Selection == 'OPP': # Checks Selection Criteria
			key = (line[FName],line[LName],line[AddressCombined],line[Zip])
			CheckDupesAndOutput()
		else:
			key = (line[VIN])
			CheckDupesAndOutput()
