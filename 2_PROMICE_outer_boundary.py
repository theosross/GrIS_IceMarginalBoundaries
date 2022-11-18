'''
This file buffers the outermost PROMICE perimeter 10 km
'''

import geopandas as gpd

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/PROMICE/"

# Read PROMICE file
gdf = gpd.read_file(filepath + 'reprojected/ice_boundary.shp')
gdf = gdf.explode()

# Export copy of only outer PROMICE perimeter
print('buffering')
outer_edge = gdf.head(1)

# Buffer
outer_edge['geometry'] = outer_edge.geometry.buffer(10000)

# Export
print('exporting')
outer_edge.to_file(filepath + 'outer/outer_buffered.shp')

edges_10km = gpd.clip(gdf, outer_edge)
edges_10km.to_file(filepath + 'reprojected/ice_boundary_10kmbuffer.shp')

