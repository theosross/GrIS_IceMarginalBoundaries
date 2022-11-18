# -*- coding: utf-8 -*-
'''
This script reprojects and filters the PROMICE ice boundary shapefile to 
EPSG: 3413 and only the main ice sheet
'''

import numpy as np
import geopandas as gpd

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/PROMICE/"

ice_boundary = gpd.read_file(filepath + 'PROMICE_250_2019-12-04.shp')

# Filter to only include main ice sheet
ice_boundary = ice_boundary[ice_boundary['GIC'] == 0]

# Give all polygons that are part of the ice sheet a value of 1
ice_boundary['GIC'] = np.where(ice_boundary['GIC'] == 0, 1, ice_boundary['GIC'])

# Merge polygons into one
ice_boundary = ice_boundary.dissolve(by='GIC')

# Convert the polygon to a polyline of the boundary
ice_boundary = ice_boundary.boundary
    
# Reproject to EPSG:3413 
ice_boundary = ice_boundary.to_crs('EPSG:3413')

# Export reprojected ice boundary
ice_boundary.to_file(filepath + 'reprojected/ice_boundary.shp')