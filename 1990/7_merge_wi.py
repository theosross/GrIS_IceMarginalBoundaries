# -*- coding: utf-8 -*-
'''
This script merges the ice-water boundary polylines
'''

import glob
import pandas
import geopandas

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2019/Classified/"
shapefiles = sorted(glob.glob(filepath + 'edges/water_ice/reprojected/*.shp'))

# Merge all shapefiles and set EPSG to 3413
gdf = pandas.concat([
    geopandas.read_file(shp)
    for shp in shapefiles
]).pipe(geopandas.GeoDataFrame)
gdf = gdf.dissolve()
gdf = gdf.explode()
gdf.to_crs('EPSG:3413')

# Export
gdf.to_file(filepath + 'merged/water_ice_merged_unedited.shp')

# Manual editing of boundaries to delete incorrect boundaries between shadows
# and ice and edit misclassified boundaries follows.
