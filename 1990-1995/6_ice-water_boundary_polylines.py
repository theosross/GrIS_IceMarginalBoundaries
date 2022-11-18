'''
This script is intended to be used within the QGIS python console.
This script converts the detected ice-water raster boundaries into polylines.
'''

import processing
import glob
from qgis.core import (
    QgsVectorLayer
)

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2005/Classified/"
files = sorted(glob.glob(filepath + 'edges/water_ice/*.tif'))

counter = 1
for raster_file in files:

    print(f'{counter} out of {len(files)}')

    inRast = raster_file
    outRast = filepath + f'edges/water_ice/masked/wil_masked_{counter}.tif'
    
    # Mask no data values
    processing.run("gdal:translate", {'INPUT':inRast,\
    'TARGET_CRS':None,'NODATA':0,'COPY_SUBDATASETS':False,\
    'OPTIONS':'','EXTRA':'','DATA_TYPE':0,'OUTPUT':outRast})

    inRast = outRast
    outRast = filepath + f'edges/water_ice/thinned/wil_edge_thinned_{counter}.tif'
    
    # Thin raster cells to make clean polyline
    processing.run("grass7:r.thin", \
    {'input':inRast,'iterations':200,'output':outRast,\
    'GRASS_REGION_PARAMETER':None,'GRASS_REGION_CELLSIZE_PARAMETER':0,\
    'GRASS_RASTER_FORMAT_OPT':'','GRASS_RASTER_FORMAT_META':''})

    inRast = outRast 
    outVect = filepath + f'edges/water_ice/polyline/wil_edge_line_{counter}.shp'
    
    # Vectorize
    processing.run("grass7:r.to.vect", \
    {'input':inRast,'type':0,'column':'value',\
    '-s':False,'-v':False,'-z':False,'-b':False,\
    '-t':False,'output':outVect,'GRASS_REGION_PARAMETER':None,\
    'GRASS_REGION_CELLSIZE_PARAMETER':0,'GRASS_OUTPUT_TYPE_PARAMETER':0,\
    'GRASS_VECTOR_DSCO':'','GRASS_VECTOR_LCO':'',\
    'GRASS_VECTOR_EXPORT_NOCAT':False})

    inVect = outVect
    outVect = filepath + f'edges/water_ice/reprojected/wil_line_repr_{counter}.shp'
    
    # Reporject to EPSG 3413
    processing.run("native:reprojectlayer", \
    {'INPUT':inVect,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:3413'),\
     'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +x_0=0 +y_0=0 +ellps=WGS84',\
     'OUTPUT':outVect})

    # Add vector layer to map
    vlayer = QgsVectorLayer(outVect, "water_ice_vector", "ogr")
    if not vlayer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)

    counter += 1



