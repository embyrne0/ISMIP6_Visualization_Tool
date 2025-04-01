'''
This is the py for extracting the data based on the fields that were choosen by the users 

* the data paths: 
"Antarctic Ice Sheet (AIS)": "/projects/grid/ghub/ISMIP6/Projections/Full_Cleaned_Projection_Data/AIS/",
"Greenland Ice Sheet (GIS)": "/projects/grid/ghub/ISMIP6/Projections/Full_Cleaned_Projection_Data/GrIS/"

* The Regions (AIS or GIS)

* 
'''
# Extracting the data of the model groups that was choosen
import os
import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import Dataset
from path import data_paths, EXPERIMENTS, VARIABLES, get_model_groups_from_files
import matplotlib.pyplot as plt
import ipywidgets as widgets

def extract_data(selected_data_path, selected_region, selected_experiment, selected_variable, selected_model_groups, selected_date_index):
    extracted_results = []  # Ensure this variable is always defined

    for model_group in selected_model_groups:
        # Parse the model_group into group and model
        group, model = model_group.split("_")  # Assuming the format is 'group_model'
        
        # Build the file path based on the naming convention with the group/model structure
        file_path = os.path.join(selected_data_path, group, model, selected_experiment, f"{selected_variable}_{selected_region}_{model_group}_{selected_experiment}.nc")
        
        # Print the file path for debugging
        print(f"Attempting to load file: {file_path}")
        
        try:
            ds = xr.open_dataset(file_path)

            # Check if the selected variable exists in the dataset
            if selected_variable in ds:
                data_extract = ds[selected_variable]
                
                # Check the time index and extract the correct time from within the variable data
                selected_time = data_extract.coords['time'].values[selected_date_index]
                print(f"Selected Time: {selected_time}")

                # Select the data for the specified time index
                selected_data = data_extract.isel(time=selected_date_index)
                
                # Determine coordinate system
                if "lon" in ds and "lat" in ds:
                    x_coord, y_coord = "lon", "lat"
                elif "x" in ds and "y" in ds:
                    x_coord, y_coord = "x", "y"
                else:
                    print(f"Error: No valid spatial coordinates found in {file_path}")
                    continue
                
                # Append the extracted data for the selected time to the result list
                extracted_results.append({
                    "time": selected_time,
                    "data": selected_data.values,  # Get the actual values (y, x) for the selected time
                    "x": ds[x_coord].values,  # Longitude or x-coordinates
                    "y": ds[y_coord].values   # Latitude or y-coordinates
                })
            else:
                print(f"Error: Variable {selected_variable} not found in {file_path}")
        
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    return extracted_results  # Return the extracted data