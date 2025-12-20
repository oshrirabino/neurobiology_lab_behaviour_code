
"""
This script generates a 2x2 dashboard plot comparing thigmotaxis index
between male and female mice for each color group (Blue, Red, Green, White),
and an additional plot showing the mean thigmotaxis index for all males vs. all females.
"""

import numpy as np
import os
import sys

# Import analysis and plotting functions from their respective modules
import data_loader
import behavioral_analysis as analysis
import behavioral_plotting as plotting

def generate_thigmotaxis_dashboard(start_sec=3, end_sec=603, bin_size=150):
    """
    Orchestrates the analysis and plotting of the thigmotaxis index dashboard.
    """
    print("\n--- Generating Thigmotaxis Index Dashboard ---")

    # 1. Load data for all animals
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data files were successfully loaded. Cannot generate dashboard.")
        return

    # 2. Run thigmotaxis analysis for all animals
    all_thigmotaxis_data = {}
    bin_centers = np.array([])

    for unit, data in loaded_data.items():
        indices, bins = analysis.calculate_thigmotaxis_in_window(data, bin_size, start_sec, end_sec)
        all_thigmotaxis_data[unit] = indices
        if bin_centers.size == 0 and bins.size > 0:
            bin_centers = bins

    # 3. Plot the dashboard if analysis yielded data
    if all_thigmotaxis_data and bin_centers.size > 0:
        plotting.plot_thigmotaxis_by_group(all_thigmotaxis_data, bin_centers)

        # 4. Calculate and plot mean thigmotaxis by sex
        male_mean, female_mean = analysis.calculate_mean_thigmotaxis_by_sex(all_thigmotaxis_data)
        plotting.plot_mean_thigmotaxis_by_sex(male_mean, female_mean, bin_centers)
    else:
        print("Error: Thigmotaxis analysis resulted in no data to plot.")

if __name__ == '__main__':
    generate_thigmotaxis_dashboard()
