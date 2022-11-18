# -*- coding: utf-8 -*-
'''
This script detects ice-water edges of classified image and exports the edges
as a GeoTIFF file.
'''

import rasterio
import numpy as np
from skimage import filters
from skimage.morphology import label
import scipy.ndimage as ndimage
import glob

# Define edge_window function that detects if edge value is a boundary between water and ice
def edge_window(array, cordinate, x_size, y_size):
    """
    Detects if edge value is a boundary between water and ice
    ----------
    Parameters:
    array : Numpy Array
        classified target array where 0 == water, 1 == ice, and 2 == land
    cordinate : Numpy Array
        edge (x,y) coordinate
    x_size : int
        size of x axis of window
    y_size : int
        size of y axis of window
    -------
    Returns:
    Boolean True or False
    """
    result = False
    
    x_left = x_size // 2
    x_right = x_left + 1
    y_bottom = y_size // 2
    y_top = y_bottom + 1
    
    x = cordinate[0]
    y = cordinate[1]
    
    edge_array = array[(x-x_left):(x+x_right), (y-y_bottom):(y+y_top)]
    
    if 2 not in edge_array: # if land not in array    
        total_pixels = x_size * y_size
        
        min_value = int((1/3) * total_pixels)
        max_value = int((2/3) * total_pixels)
        
        if np.sum(edge_array) >= min_value and np.sum(edge_array) <= max_value:
            result = True
    
    return result

###############################################################################
# Import classified images and filter them #
###############################################################################

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2019/Classified/"
files = sorted(glob.glob(filepath + 'masked_split/*.tif'))

# Open all imgaes in a loop
counter = 1
for file in files:
    print(f"{counter} out of {len(files)}")
    # Read image
    src = rasterio.open(file)
    wil_array = src.read(1)
    
    # water = 0, ice = 1, land = 2
    
    # Filter the two classified tifs
    wil_filtered = ndimage.median_filter(wil_array, size=(7, 7))
    wil_copy = np.copy(wil_filtered)
    # Set all values outside of mask (255) to nan to avoid edge detection 
    # between ice and image boundary
    wil_copy = np.where(wil_copy == 255, np.nan, wil_copy)
    # If land (2) change value to water (0), else leave as 1
    wil_copy = np.where(wil_copy == 2, 0, wil_copy)
    
    # Group ice values and eliminate all groups smaller than a certain value
    id_regions = label(wil_copy, background = 0, connectivity = 1)
    num_ids = id_regions.max()
    id_sizes = np.array(ndimage.sum(wil_copy, id_regions, range(num_ids + 1)))
    area_mask = (id_sizes < 60000)
    wil_copy[area_mask[id_regions]] = 0
    
    
    ###########################################################################
    # Edge detection between water and ice #
    ###########################################################################
    
    # Run sobel filter to detect edges between ice and other classes
    edge_sobel = filters.sobel(wil_copy)
    perimeter = np.where(edge_sobel > 0, 1, edge_sobel).astype(int)
    
    # Get coordinates where edge values are greater than 0
    edges = np.where(edge_sobel > 0)
    
    # Define x and y values of edge coordinates
    x_values = edges[0]
    y_values = edges[1]
    
    # Stack x and y value arrays to create one array of x,y coordinate pairs
    edges_cords = np.stack((x_values, y_values), axis=1)
    
    # Initialize a list for all water_ice edges as well an array of zero values
    water_ice_cords = []
    water_ice_edges = np.zeros_like(wil_array)
    
    # Loop through each coordinate pair to detect if boundary is between water and ice
    for cord_pair in edges_cords:
        if edge_window(wil_filtered, cord_pair, 5, 5):
            x = cord_pair[0]
            y = cord_pair[1]
            water_ice_edges[x, y] = 1
    
    ###########################################################################
    # Write np array as geotif file #
    ###########################################################################
    
    # If there are edges, write to a raster file
    if len(np.unique(water_ice_edges)) > 1:
        
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
        
            with rasterio.open(f'C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2019/Classified/edges/water_ice/water_ice_edges{counter}.tif', 'w', **profile) as dst:
                dst.write(water_ice_edges.astype(rasterio.uint8), 1)
           
    counter += 1
        
print('\nDone')


# *** Use qgis script after to convert to polylines ***
