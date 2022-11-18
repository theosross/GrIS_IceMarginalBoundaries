# -*- coding: utf-8 -*-
'''
This script converts all ice-water polylines to multipoint features spaced
100 m apart to calculate accurate statistics.
'''

import fiona
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
from shapely.ops import unary_union
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2019/"
shp = fiona.open(filepath + "Final_Output/greenland_glacier-water_2019.shp")

# Initialize list to store all points
all_points = [] 
counter = 1

for line in shp:
    
    print(f'{counter} out of {len(shp)}')
    if line['geometry']:
        shp_geom = shape(line['geometry'])
        
        # Define 100 m desired spacing
        distance = 100
        distances = np.arange(0, shp_geom.length, distance)
        
        # Execute converstion to multipoint feature
        points = [shp_geom.interpolate(distance) for distance in distances]
        multipoint = unary_union(points)
        
        if multipoint.type == 'MultiPoint':
            # Specify crs and append feature to list
            gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:3413', geometry=[multipoint])
            gdf['value'] = line['properties']['value']
            
            all_points.append(gdf)
    
    counter += 1

out_gdf = gpd.GeoDataFrame()

# Convert list to gdf
print('converting to gdf')
for point_gdf in all_points:
    out_gdf = out_gdf.append(point_gdf)

out_gdf = out_gdf.reset_index()
out_gdf["id"] = out_gdf.index + 1
out_gdf = out_gdf[['value', 'id', 'geometry']]

# Calculate lengths of each boundary
out_gdf_points = out_gdf['geometry'].tolist()
lengths = []
for multipoint in out_gdf_points:
    lengths.append(len(multipoint)*100)
# Add length field
out_gdf["length (m)"] = lengths

# Export
out_gdf_exploded = out_gdf.explode()
print('exporting')
out_gdf.to_file(filepath + 'Final_Output/points/2019-greenland_glacier-water_points.shp')
out_gdf_exploded.to_file(filepath + 'Final_Output/points/2019-greenland_glacier-water_points_exploded.shp')

