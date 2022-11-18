# -*- coding: utf-8 -*-
'''
This script merges the filtered, classified Greenland .tif files into one file
'''

import glob
import rasterio
from rasterio.merge import merge

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2005/Classified/"
files = sorted(glob.glob(filepath + 'filtered/*.tif'))

# Open raster files
rasters = []
for file in files:
    src = rasterio.open(file)
    rasters.append(src)

# Merge rasters
merged, out_trans = merge(rasters)

# Copy the metadata
out_meta = src.meta.copy()

# Update the metadata
out_meta.update({"driver": "GTiff", "height": merged.shape[1], \
                "dtype": rasterio.uint8, "count": 1, "compress": 'lzw',\
                "width": merged.shape[2], "transform": out_trans, \
                "crs": "EPSG:3413"})     

# Write merged rasters to file
with rasterio.open(filepath + 'merged/merged.tif', "w", **out_meta) as dest:
    dest.write(merged)