
"""
This script generates plots for locomotor activity, including accumulated total 
crossings and total crossings per bin for all animals over a 10-minute window.
"""

import numpy as np
import os
import sys

# Import analysis and plotting functions from their respective modules
import data_loader
import behavioral_analysis as analysis
import behavioral_plotting as plotting

def generate_accumulated_crossings_plot(start_sec=3, end_sec=603, bin_size=150):
    """
    Orchestrates the analysis and plotting of accumulated crossings and total crossings per bin for all animals.
    """
    print("\n--- Generating Locomotor Activity Plots ---")

    # 1. Load data for all animals
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data files were successfully loaded. Cannot generate plot.")
        return

    # 2. Run analysis for each animal
    all_accumulated_crossings = {}
    all_total_crossings = {}
    bin_centers = np.array([])
    for unit, data in loaded_data.items():
        accumulated_counts, bins = analysis.calculate_accumulated_crossings_in_window(
            data, bin_size, start_sec, end_sec
        )
        all_accumulated_crossings[unit] = accumulated_counts

        total_counts, _ = analysis.calculate_total_crossings_in_window(
            data, bin_size, start_sec, end_sec
        )
        all_total_crossings[unit] = total_counts

        if bin_centers.size == 0:
            bin_centers = bins

    # 3. Plot accumulated crossings
    if all_accumulated_crossings and bin_centers.size > 0:
        plotting.plot_accumulated_crossings_all_animals(all_accumulated_crossings, bin_centers)
    else:
        print("Warning: No accumulated crossings data to plot.")
    
    # 4. Plot total crossings
    if all_total_crossings and bin_centers.size > 0:
        plotting.plot_total_crossings_all_animals(all_total_crossings, bin_centers)
    else:
        print("Warning: No total crossings data to plot.")

if __name__ == '__main__':
    generate_accumulated_crossings_plot()
