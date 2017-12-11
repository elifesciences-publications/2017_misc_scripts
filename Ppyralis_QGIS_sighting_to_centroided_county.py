#Enable "on the fly" CRS transformation
#Add Vector Layer: cb_2016_us_county_20m
#Vector -> Geometry tools -> Polygon Centroids
#Add Vector Layer: cb_2016_us_state_20m
#Toggle editing: cb_2016_us_state_20m
#Change column NAME -> STATE_NAME in cb_2016_us_state_20m
#Processing -> Toolbox -> Add polygon attributes to points (add STATE_NAME attribute) (SAGA 2.2.3)
#This script to select only the counties that have P.pyralis
#Right click on point layer, save selection as...
#Concave hull tool with nearest neighbor = 19. Must be WGS 1984
#Load Canada vector gpr_000b11a_e

##Convert concave hull from polygon to line (Vector->Geometry->Polygons to lines)
##Smooth lines with Plugins->Generalizer->Generalizer (Chaiken's Algorithm with Level=10, and Weight = 3.00

#Vector -> Geoprocessing tools -> Clip 

#Note, at one point the Python console wouldn't open, and I had to do this: https://gis.stackexchange.com/questions/220478/qgis-python-error

#NAD83 North Dakota North (ft) (EPSG:2265)
#EPSG:4326 -> WGS84
from PyQt4.QtGui import QColor
import time


handle = open("/Users/tim/CloudSync/Weng lab/Maps/Firefly_range_map/P.pyralis range spreadsheet - Sheet1-2.csv","rU")

firefly_state_county_list = set()
headerLine = True
for line in handle.readlines():
	if headerLine == True:
		headerLine = False
		continue
	splitline = line.split(",")
	designation = splitline[4].strip().upper()
	country = splitline[5].strip().upper()
	state = splitline[6].strip().upper()
	county = splitline[7].strip().upper()
	notes = splitline[12].strip().upper()
	whole_name = state+"_"+county
	if "A" not in designation and "IGNORE" not in notes:
		firefly_state_county_list.add(whole_name)
	else:
		print "Skipping:",county,state	
handle.close()

##Iterate over all the counties
census_counties_list = set()
layer = iface.activeLayer()
selection = []
for feature in layer.getFeatures():
	county = str(feature["name"]).strip().upper()
	state = str(feature["STATE_NAME"]).strip().upper()
	whole_name = state+"_"+county
	census_counties_list.add(whole_name)
	##Select it in the GUI
	if whole_name in firefly_state_county_list:
		fid = feature.id()
		selection.append(fid)
		layer.setSelectedFeatures(selection)

good = 0
bad = 0
for wn in firefly_state_county_list:
	if wn not in census_counties_list:
		print("PROBLEM, ENTRY WITH NO HIT:",wn)
		bad +=1
	else:
		#print("A OK",wn)
		good +=1

print(good,"good and",bad,"bad")
