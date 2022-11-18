# -*- coding: utf-8 -*-
'''
This script masks the classified mosaic to the outer buffered perimeter of PROMICE
'''

import fiona
import rasterio
import rasterio.mask

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/1990/"

# Open PROMICE
with fiona.open(filepath + 'PROMICE/outer/outer_buffered.shp', "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# Mask mosaic to PROMICE
print('masking')
with rasterio.open(filepath + 'Classified/merged/merged.tif') as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, nodata=255)
    out_meta = src.meta
    out_meta.update({"driver": "GTiff", \
                    "dtype": rasterio.uint8, "count": 1, "compress": 'lzw',\
                    "crs": "EPSG:3413"})

# Export
print('exporting')
with rasterio.open(filepath + 'Classified/merged/masked.tif', "w", **out_meta) as dest:
    dest.write(out_image)


