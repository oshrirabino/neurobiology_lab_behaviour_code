import os
import scipy.io
import pandas as pd

# --- Constants ---
# The directory of this script
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# The project root directory (one level up from this script)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# The default data directory, now an absolute path
DEFAULT_DATA_DIR = os.path.join(PROJECT_ROOT, 'data_7.12')
# Default list of animal units
UNITS = ['FB', 'FG', 'FR', 'FW', 'MB', 'MG', 'MR', 'MW']
# Default rotarod data file name
DEFAULT_ROTAROD_FILE = 'rotarod_071225.xlsx'


def load_matlab_data(units=UNITS, data_dir=DEFAULT_DATA_DIR):
    """
    Loads MATLAB data for a given list of units.

    Args:
        units (list): A list of unit names (e.g., ['FB', 'MW']).
        data_dir (str): The absolute path to the directory containing the data files.

    Returns:
        dict: A dictionary where keys are the unit names and values are the loaded MATLAB data.
              If a file for a unit is not found, the corresponding value will be None.
    """
    data_map = {}
    for unit in units:
        file_name = f'{unit}_OpenField_rawdata.mat'
        file_path = os.path.join(data_dir, file_name)
        try:
            data_map[unit] = scipy.io.loadmat(file_path)
        except FileNotFoundError:
            print(f"Warning: File not found for unit '{unit}' at path: {file_path}")
            data_map[unit] = None
    return data_map


def load_rotarod_data(file_name=DEFAULT_ROTAROD_FILE, data_dir=DEFAULT_DATA_DIR):
    """
    Loads rotarod test data from an Excel file.
    
    Args:
        file_name (str): The name of the Excel file containing rotarod data.
        data_dir (str): The absolute path to the directory containing the data file.
    
    Returns:
        pd.DataFrame: A DataFrame with columns:
            - Subject_ID: The identifier of the test subject
            - Session: The session number (1-5) in chronological order
            - Latency_to_Fall: Fall latency in seconds
        Returns None if the file is not found.
    """
    file_path = os.path.join(data_dir, file_name)
    
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Filter out rows without Subject ID (empty cells or NaN)
        df = df[df['Subject ID'].notna()].copy()
        
        # Also filter out rows where Subject ID is empty string or whitespace
        df = df[df['Subject ID'].astype(str).str.strip() != ''].copy()
        
        # Combine Date and Time for sorting (with error handling for missing values)
        df['DateTime'] = pd.to_datetime(
            df['Date'].astype(str) + ' ' + df['Time'].astype(str), 
            errors='coerce'
        )
        
        # Sort by Subject_ID and DateTime
        df = df.sort_values(['Subject ID', 'DateTime']).reset_index(drop=True)
        
        # Assign session numbers chronologically for each subject
        df['Session'] = df.groupby('Subject ID').cumcount() + 1
        
        # Create clean DataFrame with only what we need
        rotarod_df = pd.DataFrame({
            'Subject_ID': df['Subject ID'],
            'Session': df['Session'],
            'Latency_to_Fall': df['Duration(sec)']
        })
        
        print(f"Successfully loaded rotarod data from {file_name}")
        print(f"Subjects: {rotarod_df['Subject_ID'].nunique()}")
        print(f"Total trials: {len(rotarod_df)}")
        
        return rotarod_df
        
    except FileNotFoundError:
        print(f"Warning: File not found at path: {file_path}")
        return None
    except Exception as e:
        print(f"Error loading rotarod data: {e}")
        return None


if __name__ == '__main__':
    # Example usage for MATLAB data:
    all_data = load_matlab_data()

    # Print the keys for the loaded data for one unit to show the structure
    if all_data and 'FB' in all_data and all_data['FB'] is not None:
        print("Successfully loaded data for FB.")
        print("Keys in the loaded data for FB:", all_data['FB'].keys())
        # Accessing data with correct keys
        if 'Freezing_start_stop' in all_data['FB']:
            print("Freezing start/stop times for FB (first 5):", all_data['FB']['Freezing_start_stop'].flatten()[:5])
        if 'crossing_times' in all_data['FB']:
            print("Crossing times for FB (first 5):", all_data['FB']['crossing_times'].flatten()[:5])

    # Example of accessing a specific unit's data
    if all_data and 'MG' in all_data and all_data['MG'] is not None:
        print("\nSuccessfully loaded data for MG.")

    # Example with a unit that doesn't exist
    print("\nAttempting to load a non-existent unit 'XX':")
    non_existent_data = load_matlab_data(['XX'])
    print("Result for 'XX':", non_existent_data['XX'])
    
    print("\n" + "="*50)
    print("Loading Rotarod Data")
    print("="*50)
    
    # Load rotarod data
    rotarod_df = load_rotarod_data()
    
    if rotarod_df is not None:
        print("\nRotarod data:")
        print(rotarod_df)