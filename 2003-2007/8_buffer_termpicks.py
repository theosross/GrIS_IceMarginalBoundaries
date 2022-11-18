# -*- coding: utf-8 -*-
'''
This script buffers the TermPick boundaries by 200 m for intersection
with ice-water boundaries
'''

import geopandas as gpd

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2003/TermPicks/"

# Combine shp files to create one all inclusive tidewater glacier boundary shp file
gdf = gpd.read_file(filepath + 'TermPicks_filtered.shp')

# Create a buffered polygon layer from your plot location points
termpicks_buffers = gdf.copy()
print('copied')

# Buffer each line using a 200 meter radius
# and replace the point geometry with the new buffered geometry
termpicks_buffers["geometry"] = gdf.geometry.buffer(200)
print('buffered')

# Export
print('exporting')
termpicks_buffers.to_file(filepath + 'buffered/TermPicks_buffered.shp')
