# -*- coding: utf-8 -*-
'''
This script calculates statistics ice-water boundary statistics 
for all three time periods.
'''

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/"
export_path = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/"

years = [2019, 2005, 1990]
region_stats = pd.DataFrame()

# Import polygon containing data gap for 1990, where statistics will be excluded
print('Reading files...')
clip_polygons = gpd.read_file(filepath + 'Year_Comparison/Clip_Polygons.shp')

# Import PROMICE boundary as points
ice_boundary_points = gpd.read_file(filepath + "PROMICE/points/points_100m_10kmbuffer.shp")
ice_boundary_points = ice_boundary_points.to_crs('EPSG:3413')

# Import region shapefile
regions_shp = gpd.read_file(filepath + "Regions/Greenland_Regions_Edited.shp")            
regions = regions_shp['SUBREGION1'].unique().tolist()

for year in years:
    if year == 2019:
        print('Calculating statistics for 2019...')
        print("Reading files...")
        
        # Import ice-water boundaries as points
        ice_water_points = gpd.read_file(filepath + "Final_Output/points/2019-greenland_glacier-water_points_exploded.shp")
        # Remove boundaries within data gap
        to_delete = []
        for ind in clip_polygons.index: # iterate over each polygon
            points_indices = ice_water_points.index.to_list()
            for index in points_indices:
                if ice_water_points.iloc[index].geometry.within(clip_polygons['geometry'][ind]):
                    to_delete.append(index)
            if len(to_delete)>0:
                ice_water_points_clipped = ice_water_points.drop(ice_water_points.index[to_delete])
        
        # Import ice-water boundaries as polylines
        ice_water_lines = gpd.read_file(filepath + "Final_Output/greenland_glacier-water_2019.shp")
        # Remove boundaries within data gap
        to_delete = []
        for ind in clip_polygons.index: # iterate over each polygon
            lines_indices = ice_water_lines.index.to_list()
            for index in lines_indices:
                if ice_water_lines.iloc[index].geometry.within(clip_polygons['geometry'][ind]):
                    to_delete.append(index)
            if len(to_delete)>0:
                ice_water_lines_clipped = ice_water_lines.drop(ice_water_lines.index[to_delete])
        
        # Calculate region statistics
        regions_dict = {}
        counter = 1
        for region in regions:
            print(f'{counter} out of {len(regions)} regions')
            region_dissolved = regions_shp.loc[regions_shp['SUBREGION1'] == region]
            
            # Intersect ice-water points with region and split into ice-lake and ice-ocean
            intersect_points = gpd.sjoin(ice_boundary_points, region_dissolved)
            intersect_water_points = gpd.sjoin(ice_water_points_clipped, region_dissolved)
            lake_points = intersect_water_points[intersect_water_points["value"] == "lake"]
            ocean_points = intersect_water_points[intersect_water_points["value"] == "ocean"]
            
            # Intersect ice-water lines with region and split into ice-lake and ice-ocean
            intersect_water_lines = gpd.sjoin(ice_water_lines_clipped, region_dissolved)
            lake_lines = intersect_water_lines[intersect_water_lines["value"] == "lake"]
            ocean_lines = intersect_water_lines[intersect_water_lines["value"] == "ocean"]
            
            # Each point = 100 m, therefore multiply number of points by 100 to get length in m and divide by 1000 to get km. (Or simply divide by 10)
            regions_dict[region] = [(len(intersect_water_points)/10),(len(lake_points)/10),(len(ocean_points)/10),(len(intersect_points)/10),\
                                    len(intersect_water_lines), len(lake_lines), len(ocean_lines)]
            counter += 1
            
        
        for region in regions_dict:
            total_length = regions_dict[region][0]
            lake_length = regions_dict[region][1]
            ocean_length = regions_dict[region][2]
            region_length = regions_dict[region][3]
            total_number = regions_dict[region][4]
            lake_number = regions_dict[region][5]
            ocean_number = regions_dict[region][6]
            
            data = {'Year':year, 'Region':region, 'Total Ice-Water Boundaries (km)':total_length,\
                    'Ice-Lake Boundaries (km)': lake_length, 'Ice-Ocean Boundaries (km)': ocean_length,\
                    'Number of Ice-Water Boundaries':total_number, 'Number of Ice-Lake Boundaries': lake_number,\
                    'Number of Ice-Ocean Boundaries':ocean_number, 'Total Region Perimeter (km)': region_length}
                
            region_stats = region_stats.append(data, ignore_index=True)
    
    elif year == 2005:
        print('Calculating statistics for 2005...')
        print("Reading files...")
        
        filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/2005/"
        
        # Import ice-water boundaries as points
        ice_water_points = gpd.read_file(filepath + "Final_Output/points/2005-greenland_glacier-water_points_exploded.shp")
        # Remove boundaries within data gap
        to_delete = []
        for ind in clip_polygons.index: # iterate over each polygon
            points_indices = ice_water_points.index.to_list()
            for index in points_indices:
                if ice_water_points.iloc[index].geometry.within(clip_polygons['geometry'][ind]):
                    to_delete.append(index)
            if len(to_delete)>0:
                ice_water_points_clipped = ice_water_points.drop(ice_water_points.index[to_delete])
        
        # Import ice-water boundaries as polylines
        ice_water_lines = gpd.read_file(filepath + "Final_Output/greenland_glacier-water_2005.shp")
        # Remove boundaries within data gap
        to_delete = []
        for ind in clip_polygons.index: # iterate over each polygon
            lines_indices = ice_water_lines.index.to_list()
            for index in lines_indices:
                if ice_water_lines.iloc[index].geometry.within(clip_polygons['geometry'][ind]):
                    to_delete.append(index)
            if len(to_delete)>0:
                ice_water_lines_clipped = ice_water_lines.drop(ice_water_lines.index[to_delete])
        
        # Calculate region statistics
        regions_dict = {}
        counter = 1
        for region in regions:
            print(f'{counter} out of {len(regions)} regions')
            region_dissolved = regions_shp.loc[regions_shp['SUBREGION1'] == region]
            
            # Intersect ice-water points with region and split into ice-lake and ice-ocean
            intersect_points = gpd.sjoin(ice_boundary_points, region_dissolved)
            intersect_water_points = gpd.sjoin(ice_water_points_clipped, region_dissolved)
            lake_points = intersect_water_points[intersect_water_points["value"] == "lake"]
            ocean_points = intersect_water_points[intersect_water_points["value"] == "ocean"]
            
            # Intersect ice-water lines with region and split into ice-lake and ice-ocean
            intersect_water_lines = gpd.sjoin(ice_water_lines_clipped, region_dissolved)
            lake_lines = intersect_water_lines[intersect_water_lines["value"] == "lake"]
            ocean_lines = intersect_water_lines[intersect_water_lines["value"] == "ocean"]
            
            # Each point = 100 m, therefore multiply number of points by 100 to get length in m and divide by 1000 to get km. (Or simply divide by 10)
            regions_dict[region] = [(len(intersect_water_points)/10),(len(lake_points)/10),(len(ocean_points)/10),(len(intersect_points)/10),\
                                    len(intersect_water_lines), len(lake_lines), len(ocean_lines)]
            counter += 1
            
        
        for region in regions_dict:
            total_length = regions_dict[region][0]
            lake_length = regions_dict[region][1]
            ocean_length = regions_dict[region][2]
            region_length = regions_dict[region][3]
            total_number = regions_dict[region][4]
            lake_number = regions_dict[region][5]
            ocean_number = regions_dict[region][6]
            
            data = {'Year':year, 'Region':region, 'Total Ice-Water Boundaries (km)':total_length,\
                    'Ice-Lake Boundaries (km)': lake_length, 'Ice-Ocean Boundaries (km)': ocean_length,\
                    'Number of Ice-Water Boundaries':total_number, 'Number of Ice-Lake Boundaries': lake_number,\
                    'Number of Ice-Ocean Boundaries':ocean_number, 'Total Region Perimeter (km)': region_length}
                
            region_stats = region_stats.append(data, ignore_index=True)
        
    else:
        print('Calculating statistics for 1990...')
        print("Reading files...")
        
        filepath = "C:/Users/theoh/Dropbox (University of Oregon)/Oregon/Glacier/1990/"
        
        # Import ice-water boundaries as points
        ice_water_points = gpd.read_file(filepath + "Final_Output/points/1990-greenland_glacier-water_points_exploded.shp")
        # Import ice-water boundaries as polylines
        ice_water_lines = gpd.read_file(filepath + "Final_Output/greenland_glacier-water_1990.shp")
        
        # Calculate region statistics
        regions_dict = {}
        counter = 1
        for region in regions:
            print(f'{counter} out of {len(regions)} regions')
            region_dissolved = regions_shp.loc[regions_shp['SUBREGION1'] == region]
            
            # Intersect ice-water points with region and split into ice-lake and ice-ocean
            intersect_points = gpd.sjoin(ice_boundary_points, region_dissolved)
            intersect_water_points = gpd.sjoin(ice_water_points, region_dissolved)
            lake_points = intersect_water_points[intersect_water_points["value"] == "lake"]
            ocean_points = intersect_water_points[intersect_water_points["value"] == "ocean"]
            
            # Intersect ice-water lines with region and split into ice-lake and ice-ocean
            intersect_water_lines = gpd.sjoin(ice_water_lines, region_dissolved)
            lake_lines = intersect_water_lines[intersect_water_lines["value"] == "lake"]
            ocean_lines = intersect_water_lines[intersect_water_lines["value"] == "ocean"]
            
            # Each point = 100 m, therefore multiply number of points by 100 to get length in m and divide by 1000 to get km. (Or simply divide by 10)
            regions_dict[region] = [(len(intersect_water_points)/10),(len(lake_points)/10),(len(ocean_points)/10),(len(intersect_points)/10),\
                                    len(intersect_water_lines), len(lake_lines), len(ocean_lines)]
            counter += 1
            
        
        for region in regions_dict:
            total_length = regions_dict[region][0]
            lake_length = regions_dict[region][1]
            ocean_length = regions_dict[region][2]
            region_length = regions_dict[region][3]
            total_number = regions_dict[region][4]
            lake_number = regions_dict[region][5]
            ocean_number = regions_dict[region][6]
            
            data = {'Year':year, 'Region':region, 'Total Ice-Water Boundaries (km)':total_length,\
                    'Ice-Lake Boundaries (km)': lake_length, 'Ice-Ocean Boundaries (km)': ocean_length,\
                    'Number of Ice-Water Boundaries':total_number, 'Number of Ice-Lake Boundaries': lake_number,\
                    'Number of Ice-Ocean Boundaries':ocean_number, 'Total Region Perimeter (km)': region_length}
                
            region_stats = region_stats.append(data, ignore_index=True)
        
# Calculate total PROMICE perimeter length, append to df
total_length = len(ice_boundary_points)/10
region_stats = region_stats.append({'Total GrIS Perimeter (km)':total_length}, ignore_index=True)

# Calculate ice-lake and ice-ocean % of perimeter for each region, round to 2 decimal points
region_stats['Ice-Lake % of Region Perimeter'] = round((region_stats['Ice-Lake Boundaries (km)'] / region_stats['Total Region Perimeter (km)']) * 100, 2)
region_stats['Ice-Ocean % of Region Perimeter'] = round((region_stats['Ice-Ocean Boundaries (km)'] / region_stats['Total Region Perimeter (km)']) * 100, 2)

print('Exporting...')
#region_stats.to_csv(export_path + 'Statistics/Year_Comparison_Stats.csv')

# Create plots of the data
x_values = [1990, 2005, 2019]
nw = region_stats[region_stats['Region'] == 'NW']
cw = region_stats[region_stats['Region'] == 'CW']
sw = region_stats[region_stats['Region'] == 'SW']
se = region_stats[region_stats['Region'] == 'SE']
ce = region_stats[region_stats['Region'] == 'CE']
ne = region_stats[region_stats['Region'] == 'NE']
no = region_stats[region_stats['Region'] == 'NO']   

nw_lakes = nw['Ice-Lake % of Region Perimeter'].to_list()[::-1]
cw_lakes = cw['Ice-Lake % of Region Perimeter'].to_list()[::-1]
sw_lakes = sw['Ice-Lake % of Region Perimeter'].to_list()[::-1]
se_lakes = se['Ice-Lake % of Region Perimeter'].to_list()[::-1]
ce_lakes = ce['Ice-Lake % of Region Perimeter'].to_list()[::-1]
ne_lakes = ne['Ice-Lake % of Region Perimeter'].to_list()[::-1]
no_lakes = no['Ice-Lake % of Region Perimeter'].to_list()[::-1]

nw_oceans = nw['Ice-Ocean % of Region Perimeter'].to_list()[::-1]
cw_oceans = cw['Ice-Ocean % of Region Perimeter'].to_list()[::-1]
sw_oceans = sw['Ice-Ocean % of Region Perimeter'].to_list()[::-1]
se_oceans = se['Ice-Ocean % of Region Perimeter'].to_list()[::-1]
ce_oceans = ce['Ice-Ocean % of Region Perimeter'].to_list()[::-1]
ne_oceans = ne['Ice-Ocean % of Region Perimeter'].to_list()[::-1]
no_oceans = no['Ice-Ocean % of Region Perimeter'].to_list()[::-1]

x_values = [1990, 2005, 2019]
plt.plot(x_values, nw_lakes, label = "nw", marker="o")
plt.plot(x_values, cw_lakes, label = "cw", marker="o")
plt.plot(x_values, sw_lakes, label = "sw", marker="o")
plt.plot(x_values, se_lakes, label = "se", marker="o")
plt.plot(x_values, ce_lakes, label = "ce", marker="o")
plt.plot(x_values, ne_lakes, label = "ne", marker="o")
plt.plot(x_values, no_lakes, label = "no", marker="o")
plt.legend()
plt.grid()
plt.xlabel("Year")
plt.ylabel("Ice-Lake % of Region Perimeter")
#plt.savefig(export_path + 'Statistics/Ice-Lake.pdf', format="pdf", bbox_inches="tight")
plt.show()

plt.plot(x_values, nw_oceans, label = "nw", marker="o")
plt.plot(x_values, cw_oceans, label = "cw", marker="o")
plt.plot(x_values, sw_oceans, label = "sw", marker="o")
plt.plot(x_values, se_oceans, label = "se", marker="o")
plt.plot(x_values, ce_oceans, label = "ce", marker="o")
plt.plot(x_values, ne_oceans, label = "ne", marker="o")
plt.plot(x_values, no_oceans, label = "no", marker="o")
plt.legend()
plt.grid()
plt.xlabel("Year")
plt.ylabel("Ice-Ocean % of Region Perimeter")
#plt.savefig(export_path + 'Statistics/Ice-Ocean.pdf', format="pdf", bbox_inches="tight")
plt.show()

