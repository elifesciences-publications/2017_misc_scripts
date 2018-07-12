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
from PyQt4.QtCore import QVariant
import time

tmpLayer = QgsVectorLayer("Point", 'test layer', "memory")  
pr = tmpLayer.dataProvider()
# define the fields of the layer
pr.addAttributes([ QgsField("Designation", QVariant.String), QgsField("Name", QVariant.String), QgsField("Notes", QVariant.String), QgsField("Date", QVariant.String), QgsField("lonEnd", QVariant.String) ])
# create a feature

handle = open("/Users/tim/CloudSync/Weng lab/Maps/Firefly_site_survey_blog_2nd/Ppyralis_range_spreadsheet.csv","rU")

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
        date = splitline[11].strip()
        latitude = splitline[8].strip()
        longitude = splitline[9].strip()
        latitude_resolution = len(latitude)-latitude.rfind(".")
        longitude_resolution = len(longitude)-longitude.rfind(".")
        print latitude_resolution,longitude_resolution
	if "IGNORE" not in notes and latitude_resolution >= 4 and longitude_resolution >=4:
                feat = QgsFeature()
                lat = float(latitude)
                long = float(longitude)
                print lat,long
		feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(long,lat)))
                feat.setAttributes([designation, county+" "+state, notes,date,"e"])
                pr.addFeatures([feat])
	else:
		print "Skipping:",county,state	
handle.close()

# update the extent of the layer
tmpLayer.updateExtents()
# update the fields
tmpLayer.updateFields()
# show the layer
QgsMapLayerRegistry.instance().addMapLayer(tmpLayer) 

