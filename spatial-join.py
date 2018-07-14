###############################################
# Date: 4/27/2018
# By: Nathaniel Douglass @ndcartography
# Version: 1.0

# Script designed to find intersect of features in two separate data sets
# Using GeoPandas Spatial Join, two datasets are merged.
# Data is then sorted based on attributes that prove the two features intersected
    
# Input args:
     # dir path to first dataset (.shp, .js, .geojson)
     # dir path to second dataset (.shp, .js, .geojson)
     # dir path to data-set output
     # dir path to point centroid output
     
# Output:
     # One polygon/line geojson for intersecting features
     # One point geojson for intersecting features
     
# Notes for next version:
	# add stats for # of features in each dataset
	# add counter for # of features found intersected
	# add print statements for data-set names
  # make centroid arg optional


'''
###############################################
 Usage:
     source activate TESTPandas python sjoin_gpd.py input_1.shp input_2.shp outpath/output_polygon(line).geojson outpath/output_centroid.geojson
###############################################
'''

import sys
import os
import geopandas as gpd

try:
    if len(sys.argv) != 5:
        sys.exit("Not enough args")

    print("Reading First file...")
    buildings = gpd.read_file(sys.argv[1])
    print("Reading Second file...")
    roads = gpd.read_file(sys.argv[2])

    print("\rCreating First GDF...")
    buildings_gdf = gpd.GeoDataFrame(buildings)
    print("\rCreating Second GDF...")
    roads_gdf = gpd.GeoDataFrame(roads)

    print("\rSPATIALLY JOINING.... Please wait... a while")
    merged_gdf = gpd.sjoin(buildings_gdf, roads_gdf, how="left", op="intersects")
    data_gdf = gpd.GeoDataFrame(merged_gdf)
    data_gdf.to_file(sys.argv[3], driver='GeoJSON')
    print('\t\tWriting Polygon Intersect to geojson for testing') 

    data = []
    data_centroid = []

    for index, orig in merged_gdf.iterrows():
        geometry = orig['geometry']
        index_right = orig['index_right']
        if orig.has_key('ID_left'):
            ID=str(orig['ID_left'])   
        elif orig.has_key('ID'):
            ID=str(orig['ID'])
        if len(str(index_right)) > 3:
            print(len(str(index_right)))
            data.append({'geometry': geometry,'ID':ID})

            ## CREATE CENTROID POINT VERSION
            geom_centroid = orig['geometry'].centroid
            data_centroid.append({'geometry': geom_centroid,'ID':ID})
   
    ### EXPORT INTERSECT DATA
    data_gdf = gpd.GeoDataFrame(data)
    data_gdf.to_file(sys.argv[3], driver='GeoJSON')
    print('\t\tWriting Polygon Intersect to geojson')    

    ### EXPORT CENTROID POINT VERSION
    cent_gdf = gpd.GeoDataFrame(data_centroid)
    cent_gdf.to_file(sys.argv[4], driver='GeoJSON')
    print('\t\tWriting Centroid Intersect to geojson')

    
except: 
    print ("Exception raised during intersection process")
    raise
