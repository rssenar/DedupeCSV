
#!/usr/bin/env python
# ---------------------------------------------
from __future__ import division, print_function
import re

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
	'Year',\
	'Make',\
	'Model',\
	'DelDate',\
	'Date',\
	'Radius',\
	'Coordinates',\
	'VINLen',\
	'DSF_WALK_SEQ',\
	'Crrt',\
	'ZipCrrt',\
	'KBB',\
	'Buyback Value',\
	'Winning Number',\
	'Mail DNQ',\
	'Blitz DNQ',\
	'Drop',\
	'Misc1',\
	'Misc2',\
	'Misc3'\
	]

def find():
	for x in range(0,len(HeaderRow)):
		if bool(re.search('.us.+ID', HeaderRow[x])):
			Customer ID = 'line[' + x + ']'
		elif bool(re.search('.ir.+ame', HeaderRow[x])):
			print('First Name')
		elif bool(re.search('MI', HeaderRow[x])):
			print('MI')
		elif bool(re.search('.as.+ame', HeaderRow[x])):
			print('Last Name')
		elif bool(re.search('.ddr.+1', HeaderRow[x])):
			print('Address1')
		elif bool(re.search('.ddr.+2', HeaderRow[x])):
			print('Address2')
		elif bool(re.search('.ddr.+', HeaderRow[x])):
			print('Address')
		elif bool(re.search('.ity', HeaderRow[x])):
			print('City')
		elif bool(re.search('.tate', HeaderRow[x])):
			print('State')
		elif bool(re.search('.ip', HeaderRow[x])):
			print('Zip')
		elif bool(re.search('4Z.+', HeaderRow[x])):
			print('Zip4')
		elif bool(re.search('SCF', HeaderRow[x])):
			print('SCF')
		elif bool(re.search('.hon.+', HeaderRow[x])):
			print('Zip')
		elif bool(re.search('.mail', HeaderRow[x])):
			print('Email')
		elif bool(re.search('VIN', HeaderRow[x])):
			print('VIN')
		elif bool(re.search('.ear', HeaderRow[x])):
			print('Year')
		elif bool(re.search('.ake', HeaderRow[x])):
			print('Make')
		elif bool(re.search('.odel', HeaderRow[x])):
			print('Model')
		elif bool(re.search('.el.+ate', HeaderRow[x])):
			print('DelDate')
		elif bool(re.search('.ate', HeaderRow[x])):
			print('Date')
		elif bool(re.search('.adi.+', HeaderRow[x])):
			print('Radius')
		elif bool(re.search('.oord.+', HeaderRow[x])):
			print('Coordinates')
		elif bool(re.search('.+Len', HeaderRow[x])):
			print('VINLen')
		elif bool(re.search('DSF.+SEQ', HeaderRow[x])):
			print('DSF_WALK_SEQ')
		elif bool(re.search('.rrt', HeaderRow[x])):
			print('Crrt')
		elif bool(re.search('.ip.+rt', HeaderRow[x])):
			print('ZipCrrt')
		elif bool(re.search('KBB', HeaderRow[x])):
			print('KBB')
		elif bool(re.search('.uyb.+Val.+', HeaderRow[x])):
			print('Buyback Value')
		elif bool(re.search('.inn.+ber', HeaderRow[x])):
			print('Winning Number')
		elif bool(re.search('.ail.+DNQ', HeaderRow[x])):
			print('Mail DNQ')
		elif bool(re.search('.lit.+DNQ', HeaderRow[x])):
			print('Blitz DNQ')
		elif bool(re.search('.rop', HeaderRow[x])):
			print('Drop')
		elif bool(re.search('.isc1', HeaderRow[x])):
			print('Misc1')
		elif bool(re.search('.isc2', HeaderRow[x])):
			print('Misc2')
		elif bool(re.search('.isc3', HeaderRow[x])):
			print('Misc3')
		else:
			print('No Match')




#print(HeaderRow[x])
'''
.(dot) = Any character
\w word character
\d digits
\s whitespace

def find(pattern, text):
	match = re.search(pattern, text)
	if match:
		print(match.group())
	else:
		print('Not Found!')

find('.ust', 'Customer ID')

HeaderRow = [\
	'Customer ID','First Name','MI','Last Name','Address1','Address2',\
	'Address','City','State','Zip','4Zip','SCF','Phone','Email','VIN','Year',\
	'Make','Model','DelDate','Date','Radius','Coordinates','VINLen',\
	'DSF_WALK_SEQ','Crrt','ZipCrrt','KBB','Buyback Value','Winning Number',\
	'Mail DNQ','Blitz DNQ','Drop','Misc1','Misc2','Misc3']
'''
