# -*- coding: utf-8 -*-
'''
This script filters the TermPick ice-ocean data to the relevant time period
'''

import geopandas as gpd

year_list = [2003,2004,2005,2006,2007]

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2005/TermPicks/"

gdf = gpd.read_file(filepath + 'TermPicks+CALFIN_V2/TermPicks+CALFIN_V2.shp')

# Sort by year
gdf.sort_values(by=['GlacierID'], inplace=True)
gdf['Date'] = gdf['Date'].astype(str)

# Get year as int object
years = []
for date in gdf['Date']:
    years.append(int(date[0:4]))

# Add df column of year to df and filter to only the years within time range
gdf['Year'] = years
gdf_out = gdf[gdf["Year"].isin(year_list)]

# Export
gdf_out.to_file(filepath + 'TermPicks_filtered.shp')



        
    
    