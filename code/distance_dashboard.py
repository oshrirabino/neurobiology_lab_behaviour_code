
"""
This script generates a 2x2 dashboard plot comparing total line crossings
between male and female mice for each color group (Blue, Red, Green, White).
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Import analysis and plotting functions from their respective modules
import data_loader
import behavioral_analysis as analysis
import behavioral_plotting as plotting

def generate_total_crossings_dashboard(start_sec=3, end_sec=603, bin_size=150):
    """
    Orchestrates the analysis and plotting of the total line crossings dashboard.

    Args:
        start_sec (int): The start time in seconds for the analysis window.
        end_sec (int): The end time in seconds for the analysis window.
        bin_size (int): The size of each analysis bin in seconds.
    """
    print("\n--- Generating Total Crossings Dashboard ---")

    # 1. Load data for all animals
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data files were successfully loaded. Cannot generate dashboard.")
        return

    # 2. Run total crossings analysis for all animals
    all_total_crossings = {}
    bin_centers = np.array([])

    for unit, data in loaded_data.items():
        total_counts, bins = analysis.calculate_total_crossings_in_window(data, bin_size, start_sec, end_sec)
        all_total_crossings[unit] = total_counts
        if bin_centers.size == 0 and bins.size > 0:
            bin_centers = bins

    # 3. Plot the dashboard if analysis yielded data
    if all_total_crossings and bin_centers.size > 0:
        plotting.plot_total_crossings_by_group(all_total_crossings, bin_centers)
    else:
        print("Error: Total crossings analysis resulted in no data to plot. Check crossing data within the 10-minute window.")

if __name__ == '__main__':
    generate_total_crossings_dashboard()
