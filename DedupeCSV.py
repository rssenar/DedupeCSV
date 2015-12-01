'''
 /$$$$$$$                /$$                            /$$$$$$  /$$$$$$ /$$    /$$
| $$__  $$              | $$                           /$$__  $$/$$__  $| $$   | $$
| $$  \ $$ /$$$$$$  /$$$$$$$/$$   /$$ /$$$$$$  /$$$$$$| $$  \__| $$  \__| $$   | $$
| $$  | $$/$$__  $$/$$__  $| $$  | $$/$$__  $$/$$__  $| $$     |  $$$$$$|  $$ / $$/
| $$  | $| $$$$$$$| $$  | $| $$  | $| $$  \ $| $$$$$$$| $$      \____  $$\  $$ $$/ 
| $$  | $| $$_____| $$  | $| $$  | $| $$  | $| $$_____| $$    $$/$$  \ $$ \  $$$/  
| $$$$$$$|  $$$$$$|  $$$$$$|  $$$$$$| $$$$$$$|  $$$$$$|  $$$$$$|  $$$$$$/  \  $/   
|_______/ \_______/\_______/\______/| $$____/ \_______/\______/ \______/    \_/    
                                    | $$                                           
                                    | $$                                           
                                    |__/                                            
'''
#!/usr/bin/python3.4.3
# Required Modules
import csv
# +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+
# |G|l|o|b|a|l| |V|a|r|i|a|b|l|e|s|
# +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
# ---------------------------------------------
InputFile = "/Users/rssenar/Desktop/" + input("File Name : ") + ".csv" 
# ---------------------------------------------
CleanOutput = "/Users/rssenar/Desktop/_CleanOutput.csv"
Dupes = "/Users/rssenar/Desktop/_Dupes.csv" 
# ---------------------------------------------
# Dedupe Criteria : 
# OPHH = One Record Per House Hold
# OPP = One Record Per Person
# VIN = Vin#
# ---------------------------------------------
Selection = 'OPHH'
# ---------------------------------------------
# Col[00] = CustomerID
# Col[01] = FirstName
# Col[02] = MI
# Col[03] = LastName
# Col[04] = Address1
# Col[05] = Address2
# Col[06] = AddressCombined
# Col[07] = City
# Col[08] = State
# Col[09] = Zip
# Col[10] = Zip + 4
# Col[11] = SCF
# Col[12] = Phone
# Col[13] = Email
# Col[14] = VIN
# Col[15] = TradeYear
# Col[16] = TradeMake
# Col[17] = TradeModel
# Col[18] = DelDate
# Col[19] = Date
# Col[20] = Radius
# Col[21] = Vin Number Length
# Col[22] = DSF_WALK_SEQ
# Col[23] = CRRT
# Col[24] = KBB
# Col[25] = Buyback Value
# Col[26] = Winning Number
# Col[27] = MailDNQ
# Col[28] = BlitzDNQ
# Col[29] = Misc1
# Col[30] = Misc2
# Col[31] = Misc3
# ---------------------------------------------
FirstName = 1
LastName = 3
Address1 = 4
Address2 = 5
AddressCombined = 6
City = 7
State = 8
Zip = 9
SCF = 11
Phone = 12
Email = 13
VIN = 14
TradeYear = 15
TradeMake = 16
TradeModel = 17
Radius = 20
VINLen = 21
WinningNum = 26
MailDNQ = 27
BlitzDNQ = 28
# ---------------------------------------------
Entries = set() # Alocate Entries set to emplty
HeaderRow = [\
	'Customer ID',\
	'First Name',\
	'MI',\
	'Last Name',\
	'Address1',\
	'Address2',\
	'Address',\
	'City',\
	'State',\
	'Zip',\
	'4Zip',\
	'SCF',\
	'Phone',\
	'Email',\
	'VIN',\
	'TradeYear',\
	'TradeMake',\
	'TradeModel',\
	'DelDate',\
	'Date',\
	'Radius',\
	'VINLen',\
	'DSF_WALK_SEQ',\
	'Crrt',\
	'KBB',\
	'Buyback Value',\
	'Winning Number',\
	'Mail DNQ',\
	'Blitz DNQ',\
	'Misc1',\
	'Misc2',\
	'Misc3'\
	]
# +-+-+-+-+-+-+-+
# |O|b|j|e|c|t|s|
# +-+-+-+-+-+-+-+ 
Input = csv.reader(open(InputFile,'r')) # Read in the input file
OutputClean = csv.writer(open(CleanOutput,'a')) # Open Clean output file
OutDupes = csv.writer(open(Dupes,'a')) # Open Dupes file
OutputClean.writerow(HeaderRow) # Append Header Row to Clean output file
OutDupes.writerow(HeaderRow) # Append Header Row to Dupes file
# +-+-+-+-+-+-+-+-+-+
# |F|u|n|c|t|i|o|n|s|
# +-+-+-+-+-+-+-+-+-+
def SetCase(): # Set case fields
	line[FirstName] = str.title(line[FirstName]) 
	line[LastName] = str.title(line[LastName])
	line[Address1] = str.title(line[Address1])
	line[Address2] = str.title(line[Address2])
	line[City] = str.title(line[City])
	line[TradeYear] = str.title(line[TradeYear])
	line[TradeMake] = str.title(line[TradeMake])
	line[TradeModel] = str.title(line[TradeModel])
	line[Email] = str.lower(line[Email])
	line[State] = str.upper(line[State])

def SetRadiusToInteger():
	if line[Radius] == "":
		line[Radius] = 9999
	else:
		line[Radius] = int(float(line[Radius]))

def SetVINLen(): # Assign the Length of the VIN# to VinLen Field
	line[VINLen] = len(line[VIN])
	if line[VINLen] < 17:
		line[VIN] = ""
	else:
		line[VIN] = str.upper(line[VIN])

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
		line[SCF] = (line[Zip])[:2] # if ZIP is less than 5 Digits
	else:
		line[SCF] = (line[Zip])[:3] # if ZIP is 5 Digits

def CheckMailDNQ():
	if line[FirstName] == "" or line[LastName] == "" or line[Radius] == 9999:
		line[MailDNQ] = "DNQ"
	else:
		line[MailDNQ] = ""

def CheckBlitzDNQ():
	if len(line[Phone]) < 8 or len(line[VIN]) < 17: 
		line[BlitzDNQ] = "DNQ"
	else:
		line[BlitzDNQ] = ""

def CheckDupeCriteriaThenOutput(): # Checks Selection Criteria
	if Selection == 'OPHH':
		key = (line[AddressCombined],line[Zip])
	elif Selection == 'OPP':
		key = (line[FirstName],line[LastName],line[AddressCombined],line[Zip])
	else:
		key = (line[VIN])
	if key not in Entries: # Check if key is in the Entries set
		OutputClean.writerow(line) # write to processed output file
		Entries.add(key) # add row to Entries set
	else:
		OutDupes.writerow(line) # write to Dupes file
# +-+-+-+-+ +-+-+-+-+-+-+-+
# |M|a|i|n| |P|r|o|g|r|a|m|
# +-+-+-+-+ +-+-+-+-+-+-+-+
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		SetCase()
		SetRadiusToInteger()
		SetVINLen()
		SetWinningNum()
		SetSCF()
		CombineAddress()
		CheckMailDNQ()
		CheckBlitzDNQ()
		CheckDupeCriteriaThenOutput()
