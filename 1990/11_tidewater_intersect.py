# -*- coding: utf-8 -*-
'''
This script
'''

import geopandas as gpd

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/1990/"

# Read in buffered TermPicks polygons
poly = gpd.read_file(filepath + 'TermPicks/buffered/TermPicks_buffered.shp')
# dissolve geometries for each glacier to merge boundaries
poly = poly.dissolve()
# explode geometries to get individual geometries for each glacier
poly = poly.explode()
poly = poly[['geometry']]

# Read in ice-water boundary polylines
lines = gpd.read_file(filepath + 'Classified/merged/water_ice_merged.shp')
lines = lines[['geometry']]
lines.dropna(inplace=True)
lines = lines.reset_index()

# Intersect join the polygons and polylines
gdf = gpd.sjoin(lines, poly)
gdf = gdf.explode()
gdf = gdf[['geometry']]
gdf.reset_index(drop=True, inplace=True)
gdf['value'] = 'ocean'

# All lines that don't intersect gien value of 'lake'
lines_out = gpd.sjoin(lines, gdf, how="left")
lines_out = lines_out[['geometry', 'value']]
lines_out['value'] = lines_out['value'].fillna('lake')
lines_out['id'] = lines_out.index + 1
lines_out = lines_out.drop_duplicates()

# Export
lines_out.to_file(filepath + 'Final_Output/greenland_glacier-water_1990.shp')