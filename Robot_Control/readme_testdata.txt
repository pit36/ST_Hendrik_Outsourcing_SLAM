The client_01.py does generate a test.csv. It has tabs as delimiters. Data does not get overwritten, Thus one has to delete old data for more compact results.

A typical row might look like this:

B	2021-06-06 22:05:12.018724	2581.475683825595	-45.05982567179065	0.0	-2.0	Enc.Wert: Distanz: 2582 Winkel: -2

The first collumn shows the source of the data: A is based on the control commands, B is based on the encoder values. 
The second collumn is a timestamp
Collumns 3,4,5 show XYZ in mm
Collumn 6 is the angle in degrees
Collumn 7 provides further comments

To seperate the test.csv into files depending on the source of the data, use the writetoseperatecsv.py
