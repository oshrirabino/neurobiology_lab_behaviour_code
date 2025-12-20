
"""
This script generates a single plot showing the Thigmotaxis Index over time
for all 8 animals on the same graph.
"""

import numpy as np
import os
import sys

# Import analysis and plotting functions from their respective modules
import data_loader
import behavioral_analysis as analysis
import behavioral_plotting as plotting

def generate_thigmotaxis_overall_plot(start_sec=3, end_sec=603, bin_size=150):
    """
    Orchestrates the analysis and plotting of the overall Thigmotaxis Index graph.
    """
    print("\n--- Generating Overall Thigmotaxis Index Plot ---")

    # 1. Load data for all animals
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data files were successfully loaded. Cannot generate plot.")
        return

    # 2. Run thigmotaxis analysis for all animals
    analyzed_thigmotaxis = {}
    bin_centers = np.array([])

    for unit, data in loaded_data.items():
        indices, bins = analysis.calculate_thigmotaxis_in_window(data, bin_size, start_sec, end_sec)
        analyzed_thigmotaxis[unit] = indices
        if bin_centers.size == 0 and bins.size > 0:
            bin_centers = bins

    # 3. Plot the graph if analysis yielded data
    if analyzed_thigmotaxis and bin_centers.size > 0:
        plotting.plot_thigmotaxis(analyzed_thigmotaxis, bin_centers)
    else:
        print("Error: Thigmotaxis analysis resulted in no data to plot.")

if __name__ == '__main__':
    generate_thigmotaxis_overall_plot()
