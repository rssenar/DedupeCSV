'''
oooooooooo.                   .o8                                     .oooooo.    .oooooo..o oooooo     oooo             ooooooooo.   ooooooooo.   
`888'   `Y8b                 "888                                    d8P'  `Y8b  d8P'    `Y8  `888.     .8'              `888   `Y88. `888   `Y88. 
 888      888  .ooooo.   .oooo888  oooo  oooo  oo.ooooo.   .ooooo.  888          Y88bo.        `888.   .8'                888   .d88'  888   .d88' 
 888      888 d88' `88b d88' `888  `888  `888   888' `88b d88' `88b 888           `"Y8888o.     `888. .8'                 888ooo88P'   888ooo88P'  
 888      888 888ooo888 888   888   888   888   888   888 888ooo888 888               `"Y88b     `888.8'                  888          888         
 888     d88' 888    .o 888   888   888   888   888   888 888    .o `88b    ooo  oo     .d8P      `888'                   888          888         
o888bood8P'   `Y8bod8P' `Y8bod88P"  `V88V"V8P'  888bod8P' `Y8bod8P'  `Y8bood8P'  8""88888P'        `8'       ooooooooooo o888o        o888o        
                                                888                                                                                                
                                               o888o                                                                                               
'''
# ---------------------------------------------
#!/usr/bin/python3.4.3
# ---------------------------------------------
# Imports
# ---------------------------------------------
import csv
# ---------------------------------------------
# Global Variables
# ---------------------------------------------
CSVFilesHaveHeaderRow = True # True or False if input files include a header row
InputFile = "DedupeSampleData.csv" 
CleanOutput = "_CleanOutputPP.csv"
Dupes = "_DupesPP.csv" 
# ---------------------------------------------w
FName = 0
LName = 1
Address = 2
Zip = 5
Entries = set()
# ----------------------------------------------
# Objects
# ----------------------------------------------
Input = csv.reader(open(InputFile,'r'))
OutputClean = csv.writer(open(CleanOutput,'a'))
OutDupes = csv.writer(open(Dupes,'a'))
OutputClean.writerow(['FName','LName','Address','City','State','Zip','VIN','Year','Make','Model'])
OutDupes.writerow(['FName','LName','Address','City','State','Zip','VIN','Year','Make','Model'])
# ----------------------------------------------
# Main Program
# ----------------------------------------------
FirstLine = True
for line in Input:
	if CSVFilesHaveHeaderRow and FirstLine:
		FirstLine = False
	else:
		key = (line[FName],line[LName],line[Address],line[Zip])
		if key not in Entries:
			OutputClean.writerow(line)
			Entries.add(key)
		else:
			OutDupes.writerow(line)
