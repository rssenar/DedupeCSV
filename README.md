### Premierworks Python ToolKit
The program runs through every record in the database and performs the following funtions:
* Check file for duplicate recrods based on Address & ZIP match
* Appends Latitude & Longitude Information then calculates straight line distance based on a central ZIP code
* Sets Proper case for the following fields: FirstName, LastName, Address1, Address2, City, TradeYear, TradeMake, TradeModel, Email, State
* Calculates VIN length. Anything less than the standard 17 characters is disregarded.
* Set winning # field value
* Created a combined field for Address1 & Address2
* Generates SCF from ZIP codes

