# -*- coding: utf-8 -*-
'''
This script converts the PROMICE outer perimeter to a multipoint feature
with spacing every 100 m for accurate calculation of statistics.

Note: This script will take ~15 minutes to execute
started 9:27
'''

import fiona
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
from shapely.ops import unary_union

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/PROMICE/"
shp = fiona.open(filepath + "reprojected/ice_boundary_10kmbuffer.shp")

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
        counter_2 = 0
        points = []
        for distance in distances:
            print(f'{counter_2} out of {len(distances)}')
            points.append(shp_geom.interpolate(distance))
            counter_2 += 1
        #points = [shp_geom.interpolate(distance) for distance in distances]
        multipoint = unary_union(points)
        
        if multipoint.type == 'MultiPoint':
            # Specify crs and append feature to list
            gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:3413', geometry=[multipoint])
            
            all_points.append(gdf)
    
    counter += 1

out_gdf = gpd.GeoDataFrame()

print('converting to gdf')
for point_gdf in all_points:
    out_gdf = out_gdf.append(point_gdf)

print('exporting')
out_gdf.to_file(filepath + 'points/points_100m_10kmbuffer.shp')
