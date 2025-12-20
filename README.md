# Lab Report Analysis and Plotting

This repository contains Python scripts to analyze and visualize behavioral data from an Open Field and Rotarod experiment with mice. Each script is designed to perform a specific analysis and generate corresponding plots.

## Required Modules and Environment

To run the scripts in this repository, you will need Python 3 and the following modules:

- `numpy`
- `pandas`
- `scipy`
- `matplotlib`
- `openpyxl`

You can install these dependencies using pip:

```bash
pip install numpy pandas scipy matplotlib openpyxl
```

## Repository Structure

The repository is organized into the following directories:

- `/code`: Contains all the Python scripts for data loading, analysis, and plotting.
- `/data_7.12`: Contains the raw experimental data in `.mat` and `.xlsx` files.
- `/plots`: The default output directory where all generated plots are saved.

## Scripts and Generated Graphs

This section details each analysis script and the graphs it produces.

---


### `accumulated_crossings_plot.py`

-   **Graphs:**
    1.  `accumulated_crossings_all.png`
    2.  `total_crossings_all.png`
-   **Description:** This script plots two graphs related to total locomotor activity. The first, "Accumulated Crossings," shows the cumulative number of total line crossings for all eight mice over a 10-minute period, which helps visualize the activity accumulation rate. The second, "Open Field - Total Locomotor Activity," shows the number of crossings per time bin for all eight mice, which illustrates the pattern of activity over time.
-   **Unique Functions Used:**
    -   `calculate_accumulated_crossings_in_window` (from `behavioral_analysis.py`): This function first calculates the number of crossings in discrete time bins and then computes a cumulative sum over these bins.
    -   `calculate_total_crossings_in_window` (from `behavioral_analysis.py`): This function calculates the number of crossings in discrete time bins.
    -   `plot_accumulated_crossings_all_animals` (from `behavioral_plotting.py`): Generates the line plot of accumulated crossings.
    -   `plot_total_crossings_all_animals` (from `behavioral_plotting.py`): Generates the line plot of total crossings per bin.

---


### `accumulated_periphery_crossings_plot.py`

-   **Graphs:**
    1.  `accumulated_periphery_crossings_all.png`
    2.  `mean_periphery_center_ratio_by_sex.png`
-   **Description:** This script generates two plots. First, it plots the cumulative number of periphery crossings for all eight mice over time. Second, it creates a bar chart comparing the mean "Periphery/Center" ratio between male and female groups. This ratio is calculated as `periphery_crossings / max(total_crossings - periphery_crossings, 1)`. The bar chart includes individual data points and SEM error bars.
-   **Unique Functions Used:**
    -   `calculate_accumulated_periphery_crossings_in_window` (from `behavioral_analysis.py`): Calculates the cumulative sum of periphery crossings in time bins.
    -   `calculate_periphery_center_ratio` (from `behavioral_analysis.py`): Calculates the periphery to center crossing ratio for each animal.
    -   `plot_accumulated_periphery_crossings_all_animals` (from `behavioral_plotting.py`): Generates the line plot of accumulated crossings.
    -   `plot_mean_periphery_center_ratio_by_sex` (from `behavioral_plotting.py`): Generates the bar chart comparing the mean periphery/center ratio between sexes.

---


### `distance_dashboard.py`

-   **Graphs:** A series of plots like `total_crossings_group_<color>.png` (e.g., `total_crossings_group_blue.png`).
-   **Description:** This script generates a dashboard of bar charts, with each chart comparing the total line crossings (a proxy for distance walked) between the male and female mouse of a specific color group (Blue, Red, Green, White). This allows for a direct comparison of activity levels between sexes within the same group.
-   **Unique Functions Used:**
    -   `calculate_total_crossings_in_window` (from `behavioral_analysis.py`): This function counts the total number of line crossing events within each 2.5-minute time bin.
    -   `plot_total_crossings_by_group` (from `behavioral_plotting.py`): This function creates and saves the bar charts for each group.

---


### `freezing_grooming_dashboard.py`

-   **Graphs:** A series of plots like `freezing_grooming_group_<color>.png` (e.g., `freezing_grooming_group_blue.png`).
-   **Description:** This script creates a dashboard of grouped bar charts that compare the duration (in seconds) of freezing and grooming behaviors. Each plot shows four bars per time bin: Male Freezing, Female Freezing, Male Grooming, and Female Grooming for a specific color group.
-   **Unique Functions Used:**
    -   `calculate_behavior_duration_in_window` (from `behavioral_analysis.py`): This versatile function is used twice here. It calculates the total duration of a given behavior (either "Freezing" or "Grooming") within each time bin by summing the lengths of event intervals that fall within that bin.
    -   `plot_freezing_grooming_by_group` (from `behavioral_plotting.py`): This function arranges the freezing and grooming data into the grouped bar chart format for each color group.

---


### `thigmotaxis_dashboard.py`

-   **Graphs:**
    1.  A series of plots like `thigmotaxis_group_<color>.png`.
    2.  `thigmotaxis_mean_by_sex.png`
-   **Description:** This script produces two kinds of visualizations for thigmotaxis (the tendency of an animal to remain close to the walls of its environment). First, it creates a dashboard of bar charts comparing the thigmotaxis index between male and female mice for each color group. Second, it generates a bar chart comparing the mean thigmotaxis index across all males versus all females.
-   **Unique Functions Used:**
    -   `calculate_thigmotaxis_in_window` (from `behavioral_analysis.py`): For each time bin, this function calculates the thigmotaxis index by dividing the number of periphery crossings by the total number of crossings.
    -   `calculate_mean_thigmotaxis_by_sex` (from `behavioral_analysis.py`): This function averages the thigmotaxis index data across all male subjects and all female subjects.
    -   `plot_thigmotaxis_by_group` (from `behavioral_plotting.py`): Creates the group-specific bar charts.
    -   `plot_mean_thigmotaxis_by_sex` (from `behavioral_plotting.py`): Creates the summary bar chart comparing the sexes.

---


### `thigmotaxis_overall_plot.py`

-   **Graph:** `thigmotaxis_over_time_10min.png`
-   **Description:** This script generates a single line graph that plots the thigmotaxis index over time for all eight animals. This provides a comprehensive overview of how this behavior evolves for each individual mouse during the experiment.
-   **Unique Functions Used:**
    -   `calculate_thigmotaxis_in_window` (from `behavioral_analysis.py`): Calculates the index for each time bin.
    -   `plot_thigmotaxis` (from `behavioral_plotting.py`): Plots the data for all animals on a single figure.

---


### `rotarod_ltf_learning_curve.py`

-   **Graphs:**
    1.  `all_subjects_learning_curves.png`
    2.  `sex_comparison_learning_curves.png`
-   **Description:** This script analyzes the rotarod performance data. It generates two plots:
    1.  A line graph showing the individual learning curve (Latency to Fall over 5 sessions) for every mouse.
    2.  A line graph comparing the mean learning curve of all male mice versus all female mice, with shaded areas representing the standard error of the mean (SEM).
-   **Unique Functions Used:**
    -   `plot_individual_learning_curves` (local to the script): Iterates through each subject's data to plot their session-by-session performance.
    -   `plot_sex_comparison` (local to the script): Groups the data by sex, calculates the mean and SEM for each session, and plots the comparative learning curves.

---


## Data Storage and Loading

### Open Field Data

-   **Storage:** The Open Field data for each mouse is stored in a separate `.mat` file (e.g., `FB_OpenField_rawdata.mat`) located in the `/data_7.12` directory. Each file contains variables like `crossing_times`, `periphery_times`, `Freezing_start_stop`, and `grooming_start_stop`.
-   **Loading:** The `load_matlab_data` function in `data_loader.py` is used to load this data. It takes a list of animal unit IDs (e.g., `['FB', 'MG']`) and returns a dictionary where keys are the unit IDs and values are the loaded data structures from the corresponding `.mat` files.

### Rotarod Data

-   **Storage:** The rotarod performance data for all subjects is stored in a single Excel file, `rotarod_071225.xlsx`, in the `/data_7.12` directory.
-   **Loading:** The `load_rotarod_data` function in `data_loader.py` reads this Excel file into a pandas DataFrame. It cleans the data, sorts trials chronologically for each subject, and assigns a `Session` number to each trial, returning a clean DataFrame ready for analysis.

## How to Run an Analysis

To run any analysis script, navigate to the `code/` directory and execute the desired script with Python.

For example, to generate the freezing and grooming dashboard:

```bash
# First, ensure you have installed the required modules
pip install numpy pandas scipy matplotlib openpyxl

# Navigate to the code directory
cd code

# Run the script
python freezing_grooming_dashboard.py
```

The script will print its progress to the console and save the resulting plots in the `/plots/freezing_grooming/` directory.

## Adding a New Analysis Script

To add a new analysis, you can create a new Python script in the `/code` directory. The following template demonstrates how to use the existing modules to create a new graph.

```python
# new_analysis_script.py

import numpy as np
import data_loader
import behavioral_analysis as analysis
import behavioral_plotting as plotting

# --- 1. Define a New Analysis Function (if needed) ---
# If the analysis is complex or unique, add a function for it in
# `behavioral_analysis.py`. For this example, let's assume we need one.
# For example, let's create a function to calculate the ratio of
# periphery to total crossings (which is thigmotaxis, but for demonstration).

def calculate_crossing_ratio(animal_data):
    """
    A new analysis function.
    This should ideally be placed in behavioral_analysis.py
    """
    total_crossings = len(animal_data['crossing_times'].flatten())
    periphery_crossings = len(animal_data['periphery_times'].flatten())
    
    if total_crossings == 0:
        return 0
    return periphery_crossings / total_crossings


# --- 2. Define a New Plotting Function (if needed) ---
# If you are creating a new type of visualization, add a function for it
# in `behavioral_plotting.py`.

def plot_new_custom_graph(data, output_filename):
    """
    A new plotting function.
    This should ideally be placed in behavioral_plotting.py
    """
    import matplotlib.pyplot as plt
    
    animals = list(data.keys())
    ratios = list(data.values())
    
    fig, ax = plt.subplots()
    ax.bar(animals, ratios)
    ax.set_title('New Analysis: Periphery Crossing Ratio')
    ax.set_ylabel('Ratio')
    
    # Save the plot
    plt.savefig(f"../plots/{output_filename}")
    print(f"Plot saved to plots/{output_filename}")
    plt.show()


# --- 3. Main script logic ---
def generate_new_plot():
    """
    Orchestrates the new analysis and plotting.
    """
    print("\n--- Generating New Custom Plot ---")

    # Load the data
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data loaded.")
        return

    # Run the new analysis for each animal
    analyzed_data = {}
    for unit, data in loaded_data.items():
        # Here we use our new "local" analysis function
        ratio = calculate_crossing_ratio(data)
        analyzed_data[unit] = ratio

    # Plot the results using our new plotting function
    if analyzed_data:
        plot_new_custom_graph(analyzed_data, "new_analysis_plot.png")
    else:
        print("Warning: No data to plot.")

if __name__ == '__main__':
    generate_new_plot()

```
To integrate this properly:
1.  Move `calculate_crossing_ratio` to `behavioral_analysis.py`.
2.  Move `plot_new_custom_graph` to `behavioral_plotting.py`.
3.  Your `new_analysis_script.py` would then import them just like the other scripts.
This modular approach ensures the codebase remains clean and reusable.
