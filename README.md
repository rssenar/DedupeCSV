### Premierworks Python ToolKit
The program runs through every record in the database and performs the following funtions:
* Check file for duplicate recrods based on Address & ZIP match
* Appends Latitude & Longitude Information then calculates straight line distance based on a central ZIP code
* Sets Proper case for the following fields: FirstName, LastName, Address1, Address2, City, TradeYear, TradeMake, TradeModel, Email, State
* Calculates VIN length. Anything less than the standard 17 characters is disregarded.
* Set winning # field value
* Created a combined field for Address1 & Address2
* Generates SCF from ZIP codes

Customer File:
* Col[00] = CustomerID
* Col[01] = FirstName
* Col[02] = MI
* Col[03] = LastName
* Col[04] = Address1
* Col[05] = Address2
* Col[06] = AddressCombined
* Col[07] = City
* Col[08] = State
* Col[09] = Zip
* Col[10] = Zip + 4
* Col[11] = SCF
* Col[12] = Phone
* Col[13] = Email
* Col[14] = VIN
* Col[15] = TradeYear
* Col[16] = TradeMake
* Col[17] = TradeModel
* Col[18] = DelDate
* Col[19] = Date
* Col[20] = Radius
* Col[21] = Coordinates
* Col[22] = Vin Number Length
* Col[23] = DSF_WALK_SEQ
* Col[24] = CRRT
* Col[25] = KBB
* Col[26] = Buyback Value
* Col[27] = Winning Number
* Col[28] = MailDNQ
* Col[29] = BlitzDNQ
* Col[30] = Misc1
* Col[31] = Misc2
* Col[32] = Misc3

Suppression File:
* Col[00] = FirstName
* Col[01] = LastName
* Col[02] = Address
* Col[03] = City
* Col[04] = State
* Col[05] = Zip
* Col[06] = Phone

Lat-Long File:
* Col[00] = zip code
* Col[01] = latitude
* Col[02] = longitude

Year Decode File:
* Col[00] = YearAbv
* Col[01] = Year

New Line