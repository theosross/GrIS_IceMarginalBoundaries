# -*- coding: utf-8 -*-
'''
This script filters the classified GeoTIFF files of Greenland
'''

import glob
import rasterio
import scipy.ndimage as ndimage

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/1990/Classified/"
files = sorted(glob.glob(filepath + 'Google_Drive/Greenland_1990/*.tif'))

count = 1
for file in files:
    
    print(f'{count} out of {len(files)}')
    
    src = rasterio.open(file)
    wil_array = src.read(1)
    
    # Filter the image
    wil_filtered = ndimage.median_filter(wil_array, size=(7, 7))
    
    with rasterio.Env():
    
        # Write an array as a raster band to a new 8-bit file. For
        # the new file's profile, we start with the profile of the source
        profile = src.profile
    
        # And then change the band counter to 1, set the
        # dtype to uint8, and specify LZW compression.
        profile.update(
            dtype=rasterio.uint8,
            counter=1,
            compress='lzw')
    
        with rasterio.open(filepath + f'filtered/image_filtered_{count}.tif', 'w', **profile) as dst:
            dst.write(wil_filtered.astype(rasterio.uint8), 1)
    
    count += 1
    