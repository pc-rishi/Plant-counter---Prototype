import arcpy
from arcpy.sa import *
from arcpy import env

arcpy.env.workspace = "Path/to/folder"


#Providing RGB Bands

red = Raster("Ortho_Band_1")
green = Raster("Ortho_Band_2")
blue = Raster("orthi_Band_3")


# Lets Apply the Index
spectral_Index = (green - blue)/(red - green)


#Threshhold to separate the features
thresh = Con(spectral_Index, 0 , 1, "Value<1")

#Smoothing Filter
smooth = Filter(thresh,"LOW", "DATA")

#Local Minima Filter
local_min = FocalStatistics(smooth, NbrRectangle(3,3,"CELL"),"MEAN","DATA")

#Spatial Aggregation
aggregator = Aggregate(smooth, 5, "MEDIAN","","DATA")



#Vectorization
polygons = arcpy.RasterToPolygon_conversion(aggregator, "Polygons.shp", "", "VALUE")

points = arcpy.FeatureToPoint_management(polygons, "Points.shp", "CENTROID")


clipper = "Rough_Boundary.shp"

Crop = arcpy.Clip_analysis(points, clipper, "study_area.shp","")


