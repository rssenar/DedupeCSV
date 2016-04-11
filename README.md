### Premierworks Python ToolKit
The Toolkit is a collection of python programs to interact and process with .csv and .xls files.  
The program runs through every record in the file and performs the following funtions:

* Select process mode Basic or Standard.
**Basic Mode** - Check file for duplicate recrods based on Address & ZIP match.
**Standard Mode** - Check file for duplicate recrods based on Address & ZIP match as well as suppression dictionaries.
- Re-Map header row if input file does not match HeaderRowMain format
- Check file for duplicate recrods based on Address & ZIP match and save to a dupes file
- Appends Latitude & Longitude Information then calculates straight line distance based on a central ZIP code
- Sets proper case for the following fields: FirstName, LastName, Address1, Address2, City, State, Year, Make, Model, Email
- Calculates VIN length. Anything less than the standard 17 characters is disregarded
- Combined Address1 & Address2 to Full Address
- Extract SCF from ZIP codes

#### Main Field Requirements:
File must contain the fields below, named as listed (fieldnames MUST BE EXACT):
- **FullName --Required--** (if first & last Names are not available)
- **FirstName --Required--**  
- **LastName --Required--** 
- **Address1 --Required--** (primary address)
- **City --Required--**
- **State --Required--**
- **ZIP --Required--** (with or without ZIP+4)

#### Additional Field Requirements for Mail Presort
- Zip4 _(10 or 9 digits or ZIP and ZIP4)_
- CRRT _(Carrier route number for Standard Mail carrier route and walk sequence mailings)_
- DSF_WALK_SEQ _(Walk sequence number for Standard Mail walk sequence mailings)_

#### Additional Fields
- Address2 _(secondary address - optional)_
- MI _(optional - Middle Initial)_
- HPhone _(optional - Home Phone#)_ 
- WPhone _(optional - Work Phone#)_
- MPhone _(optional - Mobile Phone#)_
- Email _(optional - Email Address)_
- VIN _(optional - Vehilce Identification Number)_
- Year _(optional - Vehicle Year)_
- Make _(optional - Vehicle Make)_
- Model _(optional - Vehicle Model)_
- DelDate _(optional - Vehicle Delivery Date / Sales Date)_
- Date _(optional - Last Service Date)_
- KBB _(optional - Kelly Blue Book Value)_
- BuybackValues _(optional - Adjusted Kelly Blue Book Value)_
- PURL _(optional - Personal URL)_
- Misc1 _(optional- extra field 1)_
- Misc2 _(optional- extra field 2)_
- Misc3 _(optional- extra field 3)_

