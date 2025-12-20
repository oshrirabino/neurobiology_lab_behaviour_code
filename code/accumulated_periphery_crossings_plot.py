
"""
This script generates a plot showing the accumulated periphery crossings for all animals
over a 10-minute window, with 150-second bins, and a plot of the mean periphery/center ratio by sex.
"""

import numpy as np
import os
import sys

# Import analysis and plotting functions from their respective modules
import data_loader
import behavioral_analysis as analysis
import behavioral_plotting as plotting

def generate_accumulated_periphery_crossings_plot(start_sec=3, end_sec=603, bin_size=150):
    """
    Orchestrates the analysis and plotting of accumulated periphery crossings for all animals
    and the mean periphery/center ratio by sex.
    """
    print("\n--- Generating Accumulated Periphery Crossings and Ratio Plots ---")

    # 1. Load data for all animals
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data files were successfully loaded. Cannot generate plot.")
        return

    # 2. Run analysis for each animal
    all_accumulated_periphery_crossings = {}
    all_ratios = {}
    bin_centers = np.array([])
    for unit, data in loaded_data.items():
        accumulated_counts, bins = analysis.calculate_accumulated_periphery_crossings_in_window(
            data, bin_size, start_sec, end_sec
        )
        all_accumulated_periphery_crossings[unit] = accumulated_counts
        if bin_centers.size == 0:
            bin_centers = bins
        
        ratio = analysis.calculate_periphery_center_ratio(data, start_sec, end_sec)
        all_ratios[unit] = ratio


    # 3. Plot accumulated periphery crossings
    if all_accumulated_periphery_crossings and bin_centers.size > 0:
        plotting.plot_accumulated_periphery_crossings_all_animals(all_accumulated_periphery_crossings, bin_centers)
    else:
        print("Warning: No data to plot for accumulated periphery crossings.")
        
    # 4. Plot mean periphery/center ratio
    if all_ratios:
        plotting.plot_mean_periphery_center_ratio_by_sex(all_ratios)
    else:
        print("Warning: No data to plot for mean periphery/center ratio.")

if __name__ == '__main__':
    generate_accumulated_periphery_crossings_plot()
