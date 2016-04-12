
import re
# ---------------------------------------------------------------------------- #
# Set Constant Variables
SeqNumDatabase = 10000
SeqNumPurchaseP = 30000
SeqNumPurchaseN = 40000
SeqNumPurchase = 50000
# ---------------------------------------------------------------------------- #
CustomerID = 0
FullName = 1
FirstName = 2
MI = 3
LastName = 4
Address1 = 5
Address2 = 6
AddressComb = 7
City = 8
State = 9
Zip = 10
Zip4 = 11
SCF = 12
Phone = 13
HPhone = 14
WPhone = 15
MPhone = 16
Email = 17
VIN = 18
Year = 19
Make = 20
Model = 21
DelDate = 22
Date = 23
Radius = 24
Coordinates = 25
VINLen = 26
DSF_WALK_SEQ = 27
CRRT = 28
ZipCRRT = 29
KBB = 30
BuybackValues = 31
WinningNum = 32
MailDNQ = 33
BlitzDNQ = 34
Drop = 35
PURL = 36
SCF3DFacility = 37
Vendor = 38
Misc1 = 39
Misc2 = 40
Misc3 = 41
# ---------------------------------------------------------------------------- #
# Header Output list
HeaderRowMain = [
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
	'SCF3DFacility',
	'Vendor',
	'Misc1',
	'Misc2',
	'Misc3'
	]
# ---------------------------------------------------------------------------- #
HeaderDict = {}
def MatchHeaderFields(field, index):
	if bool(re.search('ful.+me',field,flags=re.I)):
		HeaderDict[FullName] = 'line[{}]'.format(str(index))
	elif bool(re.search('fir.+me',field,flags=re.I)):
		HeaderDict[FirstName] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bmi\b',field,flags=re.I)):
		HeaderDict[MI] = 'line[{}]'.format(str(index))
	elif bool(re.search('las.+me',field,flags=re.I)):
		HeaderDict[LastName] = 'line[{}]'.format(str(index))
	elif bool(re.search('addr.+1',field,flags=re.I)):
		HeaderDict[Address1] = 'line[{}]'.format(str(index))
	elif bool(re.search('addr.+2',field,flags=re.I)):
		HeaderDict[Address2] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bcity\b',field,flags=re.I)):
		HeaderDict[City] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bstate\b',field,flags=re.I)):
		HeaderDict[State] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bzip\b',field,flags=re.I)):
		HeaderDict[Zip] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\b4zip\b',field,flags=re.I)) or\
	bool(re.search(r'\bzip4\b',field,flags=re.I)):
		HeaderDict[Zip4] = 'line[{}]'.format(str(index))
	elif bool(re.search('HPho.+',field,flags=re.I)) or\
	bool(re.search(r'\bhph\b',field,flags=re.I)):
		HeaderDict[HPhone] = 'line[{}]'.format(str(index))
	elif bool(re.search('WPho.+',field,flags=re.I)) or\
	bool(re.search(r'\bbph\b',field,flags=re.I)):
		HeaderDict[WPhone] = 'line[{}]'.format(str(index))
	elif bool(re.search('MPho.+',field,flags=re.I)) or\
	bool(re.search(r'\bcph\b',field,flags=re.I)):
		HeaderDict[MPhone] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bemail\b',field,flags=re.I)):
		HeaderDict[Email] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bvin\b',field,flags=re.I)):
		HeaderDict[VIN] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\byear\b',field,flags=re.I)) or\
	bool(re.search(r'\bvyr\b',field,flags=re.I)):
		HeaderDict[Year] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bmake\b',field,flags=re.I)) or\
	bool(re.search(r'\bvmk\b',field,flags=re.I)):
		HeaderDict[Make] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bmodel\b',field,flags=re.I)) or\
	bool(re.search(r'\bvmd\b',field,flags=re.I)):
		HeaderDict[Model] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bdeldate\b',field,flags=re.I)):
		HeaderDict[DelDate] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bdate\b',field,flags=re.I)):
		HeaderDict[Date] = 'line[{}]'.format(str(index))
	elif bool(re.search('dsf.+seq',field,flags=re.I)):
		HeaderDict[DSF_WALK_SEQ] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bcrrt\b',field,flags=re.I)):
		HeaderDict[CRRT] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bkbb\b',field,flags=re.I)):
		HeaderDict[KBB] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bbuybackvalue\b',field,flags=re.I)):
		HeaderDict[BuybackValues] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bpurl\b',field,flags=re.I)):
		HeaderDict[PURL] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bmisc1\b',field,flags=re.I)):
		HeaderDict[Misc1] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bmisc2\b',field,flags=re.I)):
		HeaderDict[Misc2] = 'line[{}]'.format(str(index))
	elif bool(re.search(r'\bmisc3\b',field,flags=re.I)):
		HeaderDict[Misc3] = 'line[{}]'.format(str(index))
# ---------------------------------------------------------------------------- #
# Function to Generate ConvPercentage Value
def ConvPercentage(part, whole):
	if whole == 0:
		return 0
	else:
		return 100 * float(part)/float(whole)

# Function to Convert String To List
def ConvertStringToList(input):
	AppendedList = []
	input = input.split('|')
	for item in input:
		item = item.strip()
		item = str.lower(item)
		AppendedList.append(item)
	return AppendedList

# Function to Reformat Phone Number and strip white space and extra char
def ReformatPhoneNum(Phone):
	Phone = str(Phone).strip()
	Phone = str(Phone).replace('-','')
	Phone = str(Phone).replace('(','')
	Phone = str(Phone).replace(')','')
	return Phone

# Convert list item to string
def ConvListToString(input):
	for item in input:
		return item
# ---------------------------------------------------------------------------- #
DoNotMailSet = set([
	'inc', 'inc.', 'incorporated', 'international', 'corporation', 'corp', 
	'corp.', 'construction', 'const', 'const.', 'prof', 'prof.', 'professional', 
	'service', 'services', 'consultancy', 'consultant', 'consultants', 'living', 
	'trust', 'llc', 'enterprise', 'enterprises', 'infrastructure', 'the', 
	'resource', 'resources', 'cooperative', 'cooperatives', 'comp', 'company', 
	'companies', 'store', 'dealer', 'dealers', 'dealership', 'dealerships', 
	'fleet', 'office', 'station', 'health', 'acura', 'am general', 'audi', 
	'bmw', 'buick', 'cadillac', 'chevrolet', 'chrysler', 'daewoo', 'dodge', 
	'ferrari', 'fiat', 'gmc', 'honda', 'hummer', 'hyundai', 'infiniti', 'isuzu', 
	'jaguar', 'jeep', 'kia', 'land rover', 'lexus', 'lincoln', 'maserati', 
	'maybach', 'mazda', 'mercedes', 'mercedes-benz', 'mercury', 'mini', 
	'mitsubishi', 'nissan', 'oldsmobile', 'plymouth', 'pontiac', 'porsche',
	'ram', 'saab', 'saturn', 'scion', 'smart', 'subaru', 'suzuki', 'toyota',
	'volkswagen', 'volvo', 'auto', 'automotive', 'group' 
	])

YearDecodeDict = dict([
	(0,2000), (1,2001), (2,2002), (3,2003), (4,2004), (5,2005), (6,2006), 
	(7,2007), (8,2008), (9,2009), (10,2010), (11,2011), (12,2012), (13,2013), 
	(14,2014), (15,2015), (16,2016), (17,2017), (18,2018), (19,2019), (20,2020), 
	(40,1940), (41,1941), (42,1942), (43,1943), (44,1944), (45,1945), (46,1946), 
	(47,1947), (48,1948), (49,1949), (50,1950), (51,1951), (52,1952), (53,1953), 
	(54,1954), (55,1955), (56,1956), (57,1957), (58,1958), (59,1959), (60,1960), 
	(61,1961), (62,1962), (63,1963), (64,1964), (65,1965), (66,1966), (67,1967), 
	(68,1968), (69,1969), (70,1970), (71,1971), (72,1972), (73,1973), (74,1974), 
	(75,1975), (76,1976), (77,1977), (78,1978), (79,1979), (80,1980), (81,1981), 
	(82,1982), (83,1983), (84,1984), (85,1985), (86,1986), (87,1987), (88,1988), 
	(89,1989), (90,1990), (91,1991), (92,1992), (93,1993), (94,1994), (95,1995), 
	(96,1996), (97,1997), (98,1998), (99,1999)
	])

USStatesDict = {
	'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa',
	'AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut',
	'DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia',
	'GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois',
	'IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts',
	'MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri',
	'MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National',
	'NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire',
	'NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio',
	'OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico',
	'RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee',
	'TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont',
	'WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'
	}

