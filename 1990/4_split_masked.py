# -*- coding: utf-8 -*-
'''
This script splits the masked, classified mosaic into smaller
tiles for processing
'''

import gdal
import os

# Define directory
os.chdir("C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/1990/")

# Read files, set output
in_path = "Classified/merged/"
input_filename = 'masked.tif'
out_path = "Classified/masked_split/"
output_filename = 'image_'

tile_size_x = 10000
tile_size_y = 10000

ds = gdal.Open(in_path + input_filename)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize

# Create files and export
print('splitting masked image into smaller sizes for processing')
for i in range(0, xsize, tile_size_x):
    print(f"{i} out of {xsize}")
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + \
            str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + \
                " " + str(in_path) + str(input_filename) + " " + \
                    str(out_path) + str(output_filename) + str(i) + "_" + \
                        str(j) + ".tif"
        os.system(com_string)