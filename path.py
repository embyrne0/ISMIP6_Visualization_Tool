# path.py
import os
import re
from pathlib import Path

# Define the available data paths
data_paths = {
    "Antarctic Ice Sheet (AIS)": "/projects/grid/ghub/ISMIP6/Projections/Full_Cleaned_Projection_Data/AIS/",
    "Greenland Ice Sheet (GIS)": "/projects/grid/ghub/ISMIP6/Projections/Full_Cleaned_Projection_Data/GrIS/"
    # "Greenland Ice Sheet (GIS)": "D:/Thesis_Gl_Projections" # practice 
}

# Define experiments for each region
EXPERIMENTS = {
    "Greenland Ice Sheet (GIS)": ["asmb", "ctrl", "ctrl_proj", "historical"],
    "Antarctic Ice Sheet (AIS)": ["asmb", "ctrl", "ctrl_proj", "historical"]
}


# Variables (only acabf for now)
VARIABLES = ["acabf", "lithk"] 

# Function to get model groups based on path, experiment, and variable
def get_model_groups_from_files(path: str, experiment: str, variable: str) -> list:
    """Get model group names from file paths based on the naming structure."""
    model_groups = set()  # Use a set to avoid duplicates
    pattern = r'(?P<field>\w+)_(?P<region>\w+)_(?P<group>\w+)_(?P<model>\w+)_(?P<exp>\w+)\.nc'
    path_obj = Path(path)

    if not path_obj.exists():
        print(f"Warning: The path {path} does not exist.")
        return []

    for file in path_obj.rglob("*.nc"):
        match = re.search(pattern, file.name)  # Match regex pattern in file name
        if match:
            field = match.group("field")
            region = match.group("region")
            group = match.group("group")  # Extract model group
            model = match.group("model")
            exp = match.group("exp")

            # Filter files by experiment and variable
            if exp == experiment and field == variable:
                model_groups.add(f"{group}_{model}")

    return sorted(list(model_groups))  # Return as a sorted list
    
# def create_path_selector():
#     """Creates and returns a dropdown widget for selecting the data path."""
#     path_selector = widgets.Dropdown(
#         options=data_paths.keys(),  # ✅ Use dataset names (keys)
#         description="Select Path:",
#         disabled=False, 
#         style={'description_width': 'initial'},
#         layout=widgets.Layout(width='500px')
#     )
#     return path_selector