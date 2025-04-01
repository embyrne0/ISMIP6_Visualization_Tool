import ipywidgets as widgets
from IPython.display import display
from path import data_paths, EXPERIMENTS, VARIABLES, get_model_groups_from_files
from data_extraction import extract_data

# Widgets
data_path_selector = widgets.Dropdown(
    options=["Select Path", "Antarctic Ice Sheet (AIS)", "Greenland Ice Sheet (GIS)"],
    value="Select Path",
    description="Select Data Path:"
)

experiment_selector = widgets.RadioButtons(
    options=["Select Experiment"],  # Placeholder options until path is selected
    description="Select Experiment:",
    disabled=False
)

variable_selector = widgets.RadioButtons(
    options=["Select Variable"],  # Placeholder options until experiment is selected
    description="Select Variable:", 
    disabled=False
)


model_group_selector = widgets.SelectMultiple(
    options=["Select Model Group"],  # Placeholder until variable is selected
    description="Select Model Group:"
    
)

# Date selector widget (index from 0 to 86)
date_selector = widgets.BoundedIntText(
    name='Time Step',
    min=0,
    max=86,
    step=1,
    description="Select Date Index:", 
    continuous_update=False
)

# Button to confirm model group selection
confirm_button = widgets.Button(description="Confirm Model Group Selection")

# Button to confirm date selection
date_confirm_button = widgets.Button(description="Confirm Date Selection")

# Clear/Reset Button
clear_button = widgets.Button(
    description="Clear/Reset",
    button_style="warning",  # Optional style
    tooltip="Click to reset all selections"
)

# Function to update experiment options based on selected data path
def update_experiment_options(change):
    selected_path = data_path_selector.value
    if selected_path != "Select Path":
        experiments = EXPERIMENTS.get(selected_path, [])
        # Add a blank option to ensure no experiment is selected by default
        experiment_selector.options = ["Select Experiment"] + experiments
        experiment_selector.value = "Select Experiment"  # Ensure no experiment is selected by default
        experiment_selector.disabled = False
    else:
        experiment_selector.options = ["Select Experiment"]
        experiment_selector.value = "Select Experiment"  # Ensure it's reset
        experiment_selector.disabled = True
        # Reset variable and model group directly
        variable_selector.options = ["Select Variable"]
        variable_selector.value = "Select Variable"
        variable_selector.disabled = True
        model_group_selector.options = ["Select Model Group"]
        model_group_selector.value = "Select Model Group"
        model_group_selector.disabled = True

# Function to update variable options based on selected experiment
def update_variable_options(change):
    selected_experiment = experiment_selector.value
    if selected_experiment != "Select Experiment":
        variable_selector.options = ["Select Variable"] + VARIABLES  # Add a blank option to ensure no variable is selected by default
        variable_selector.value = "Select Variable"  # Ensure no variable is selected by default
        variable_selector.disabled = False
    else:
        variable_selector.options = ["Select Variable"]
        variable_selector.value = "Select Variable"  # Ensure it's reset
        variable_selector.disabled = True
        model_group_selector.disabled = True

def update_model_group_options(change):
    selected_variable = variable_selector.value
    selected_experiment = experiment_selector.value
    selected_path = data_path_selector.value
    
    print(f"Selected Path: {selected_path}, Selected Experiment: {selected_experiment}, Selected Variable: {selected_variable}")
    
    if selected_variable != "Select Variable" and selected_experiment != "Select Experiment":
        model_groups = get_model_groups_from_files(
            data_paths[selected_path], selected_experiment, selected_variable
        )
        
        print(f"Model Groups Found: {model_groups}")
        
        model_group_selector.options = ["Select Model Group"] + model_groups  # Add blank option to ensure nothing is selected by default
        model_group_selector.disabled = False
    else:
        model_group_selector.options = ["Select Model Group"]
        model_group_selector.disabled = True

# Function to reset all selections when "Clear/Reset" button is clicked
def reset_all_selections(b):
    data_path_selector.value = "Select Path"
    experiment_selector.value = "Select Experiment"
    experiment_selector.disabled = True
    variable_selector.value = "Select Variable"
    variable_selector.disabled = True
    
   # For SelectMultiple, set the value as an empty tuple or default selected options tuple
    model_group_selector.value = ("Select Model Group",)  # Ensure it's a tuple, even if only one option is available
    
    date_selector.disabled = True
    date_confirm_button.disabled = True
    
# Function to handle model group confirmation
def on_model_group_confirm(b):
    selected_model_groups = model_group_selector.value
    print(f"Selected Model Group(s): {selected_model_groups}")
    
    # Enable date selection and confirm button
    date_selector.disabled = False
    date_confirm_button.disabled = False

# Function to handle date confirmation and proceed to data extraction and visualization
def on_date_confirm_button_click(b):
    # Ensure selected path exists in data_paths
    selected_data_path = data_paths.get(data_path_selector.value, None)
    if not selected_data_path:
        print("Error: Invalid data path selected.")
        return

    selected_experiment = experiment_selector.value
    selected_variable = variable_selector.value
    selected_model_groups = list(model_group_selector.value)  # Convert tuple to list
    selected_date_index = date_selector.value
    
    # Debug prints to check the parameters
    print(f"Selected Date Index: {selected_date_index}")
    print(f"Selected Data Path: {selected_data_path}")
    print(f"Selected Experiment: {selected_experiment}")
    print(f"Selected Variable: {selected_variable}")
    print(f"Selected Model Groups: {selected_model_groups}")

# Call the extract_data function to get the data
    extracted_data = extract_data(
        selected_data_path, 
        selected_experiment, 
        selected_variable, 
        selected_model_groups, 
        selected_date_index  # Pass the selected date index
    )
    
    if extracted_data:
        print("Proceeding to data extraction and visualization...")
        # Convert extracted data to DataFrame if needed
        extracted_df = pd.DataFrame(extracted_data)
        print(extracted_df.head())  # Show a preview of the extracted data
    else:
        print("No data extracted. Please check your selections.")

# Link widget functions to widget changes
data_path_selector.observe(update_experiment_options, names='value')
experiment_selector.observe(update_variable_options, names='value')
variable_selector.observe(update_model_group_options, names='value')

clear_button.on_click(reset_all_selections)

# Link confirm button to model group confirmation
confirm_button.on_click(on_model_group_confirm)

# Link date confirm button to data extraction and visualization
date_confirm_button.on_click(on_date_confirm_button_click)

# Function to display all widgets
def display_widgets():
    display(data_path_selector, experiment_selector, variable_selector, model_group_selector, confirm_button, date_selector, date_confirm_button, clear_button)