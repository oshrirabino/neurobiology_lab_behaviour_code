
"""
This script generates a 2x2 dashboard plot comparing freezing and grooming
durations between male and female mice for each color group.
"""

import numpy as np
import os
import sys

# Import analysis and plotting functions from their respective modules
import data_loader
import behavioral_analysis as analysis
import behavioral_plotting as plotting

def generate_freezing_grooming_dashboard(start_sec=3, end_sec=603, bin_size=150):
    """
    Orchestrates the analysis and plotting of the freezing/grooming dashboard.
    """
    print("\n--- Generating Freezing & Grooming Dashboard ---")

    # 1. Load data for all animals
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data files were successfully loaded. Cannot generate dashboard.")
        return

    # 2. Run analysis for freezing and grooming for all animals
    all_freezing_data = {}
    all_grooming_data = {}
    bin_centers = np.array([])

    for unit, data in loaded_data.items():
        # Freezing
        freezing_durations, bins = analysis.calculate_behavior_duration_in_window(data, 'Freezing_start_stop', bin_size, start_sec, end_sec)
        all_freezing_data[unit] = freezing_durations
        if bin_centers.size == 0 and bins.size > 0:
            bin_centers = bins
            
        # Grooming
        grooming_durations, _ = analysis.calculate_behavior_duration_in_window(data, 'grooming_start_stop', bin_size, start_sec, end_sec)
        all_grooming_data[unit] = grooming_durations

    # 3. Plot the dashboard if analysis yielded data
    if all_freezing_data and all_grooming_data and bin_centers.size > 0:
        plotting.plot_freezing_grooming_by_group(all_freezing_data, all_grooming_data, bin_centers)
        plotting.plot_freezing_grooming_all_animals(all_freezing_data, all_grooming_data, bin_centers)
    else:
        print("Error: Analysis resulted in no data to plot.")

if __name__ == '__main__':
    generate_freezing_grooming_dashboard()
