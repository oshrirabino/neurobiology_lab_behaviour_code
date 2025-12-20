
"""
This module provides functions for analyzing the experimental data.
When run as a script, it performs all analyses and calls the plotting
module to generate individual plots for each metric.
"""

import numpy as np
import data_loader
import behavioral_plotting

# --- Analysis Functions ---

def calculate_thigmotaxis_in_window(animal_data, bin_size_seconds=150, start_time_seconds=3, end_time_seconds=603):
    """
    Analyzes a single animal's data to calculate the thigmotaxis index over a fixed time window.
    """
    all_crossings = animal_data['crossing_times'].flatten()
    periphery_crossings = animal_data['periphery_times'].flatten()

    time_window_mask = (all_crossings >= start_time_seconds) & (all_crossings < end_time_seconds)
    all_crossings_in_window = all_crossings[time_window_mask]

    periphery_mask = (periphery_crossings >= start_time_seconds) & (periphery_crossings < end_time_seconds)
    periphery_crossings_in_window = periphery_crossings[periphery_mask]
    
    duration = end_time_seconds - start_time_seconds
    bins = np.arange(0, duration + bin_size_seconds, bin_size_seconds)
    bin_ends_minutes = bins[1:] / 60

    total_counts, _ = np.histogram(all_crossings_in_window - start_time_seconds, bins=bins)
    periphery_counts, _ = np.histogram(periphery_crossings_in_window - start_time_seconds, bins=bins)

    thigmotaxis_indices = np.divide(periphery_counts, total_counts, 
                                    out=np.full_like(total_counts, np.nan, dtype=float), 
                                    where=total_counts!=0)
    
    thigmotaxis_indices = np.nan_to_num(thigmotaxis_indices, nan=0.0)
    thigmotaxis_indices = np.minimum(thigmotaxis_indices, 1.0)

    return thigmotaxis_indices, bin_ends_minutes

def calculate_behavior_duration_in_window(animal_data, behavior_key, bin_size_seconds=150, start_time_seconds=3, end_time_seconds=603):
    """
    Calculates the total duration of a specific behavior within each bin of a fixed time window.
    """
    if behavior_key not in animal_data or animal_data[behavior_key].size == 0:
        duration = end_time_seconds - start_time_seconds
        num_bins = int(duration / bin_size_seconds)
        bins = np.arange(0, duration + bin_size_seconds, bin_size_seconds)
        bin_ends_minutes = bins[1:] / 60
        return np.zeros(num_bins), bin_ends_minutes

    behavior_times = animal_data[behavior_key]
    duration = end_time_seconds - start_time_seconds
    bins = np.arange(start_time_seconds, end_time_seconds + bin_size_seconds, bin_size_seconds)
    binned_durations = np.zeros(len(bins) - 1)

    for i in range(len(bins) - 1):
        bin_start, bin_end = bins[i], bins[i+1]
        overlap_start = np.maximum(behavior_times[0, :], bin_start)
        overlap_end = np.minimum(behavior_times[1, :], bin_end)
        overlap_duration = np.maximum(0, overlap_end - overlap_start)
        binned_durations[i] = np.sum(overlap_duration)
        
    bin_ends_minutes = (bins[1:] - start_time_seconds) / 60
    
    return binned_durations, bin_ends_minutes

def calculate_total_crossings_in_window(animal_data, bin_size_seconds=150, start_time_seconds=3, end_time_seconds=603):
    """
    Calculates the total number of line crossings in each bin of a fixed time window.
    
    Args:
        animal_data (dict): The raw data for one animal, as loaded from its .mat file.
        bin_size_seconds (int): The size of each time bin in seconds.
        start_time_seconds (int): The start of the analysis window in seconds.
        end_time_seconds (int): The end of the analysis window in seconds.

    Returns:
        tuple: A tuple containing:
            - total_counts (np.array): The number of crossings in each bin.
            - bin_ends_minutes (np.array): The end of each time bin in minutes, for the x-axis.
    """
    all_crossings = animal_data['crossing_times'].flatten()

    # Filter crossings to be within the specified time window
    time_window_mask = (all_crossings >= start_time_seconds) & (all_crossings < end_time_seconds)
    all_crossings_in_window = all_crossings[time_window_mask]
    
    # Create time bins relative to the start time
    duration = end_time_seconds - start_time_seconds
    bins = np.arange(0, duration + bin_size_seconds, bin_size_seconds)
    bin_ends_minutes = bins[1:] / 60

    # Adjust timestamps to be relative to the start of the window for binning
    total_counts, _ = np.histogram(all_crossings_in_window - start_time_seconds, bins=bins)
    
    return total_counts, bin_ends_minutes

def calculate_accumulated_crossings_in_window(animal_data, bin_size_seconds=150, start_time_seconds=3, end_time_seconds=603):
    """
    Calculates the accumulated number of line crossings in each bin of a fixed time window.
    
    Args:
        animal_data (dict): The raw data for one animal, as loaded from its .mat file.
        bin_size_seconds (int): The size of each time bin in seconds.
        start_time_seconds (int): The start of the analysis window in seconds.
        end_time_seconds (int): The end of the analysis window in seconds.

    Returns:
        tuple: A tuple containing:
            - accumulated_counts (np.array): The accumulated number of crossings in each bin.
            - bin_ends_minutes (np.array): The end of each time bin in minutes, for the x-axis.
    """
    total_counts, bin_ends_minutes = calculate_total_crossings_in_window(
        animal_data, bin_size_seconds, start_time_seconds, end_time_seconds
    )
    accumulated_counts = np.cumsum(total_counts)
    return accumulated_counts, bin_ends_minutes

def calculate_periphery_crossings_in_window(animal_data, bin_size_seconds=150, start_time_seconds=3, end_time_seconds=603):
    """
    Calculates the total number of periphery line crossings in each bin of a fixed time window.
    
    Args:
        animal_data (dict): The raw data for one animal, as loaded from its .mat file.
        bin_size_seconds (int): The size of each time bin in seconds.
        start_time_seconds (int): The start of the analysis window in seconds.
        end_time_seconds (int): The end of the analysis window in seconds.

    Returns:
        tuple: A tuple containing:
            - periphery_counts (np.array): The number of periphery crossings in each bin.
            - bin_ends_minutes (np.array): The end of each time bin in minutes, for the x-axis.
    """
    periphery_crossings = animal_data['periphery_times'].flatten()

    # Filter crossings to be within the specified time window
    time_window_mask = (periphery_crossings >= start_time_seconds) & (periphery_crossings < end_time_seconds)
    periphery_crossings_in_window = periphery_crossings[time_window_mask]
    
    # Create time bins relative to the start time
    duration = end_time_seconds - start_time_seconds
    bins = np.arange(0, duration + bin_size_seconds, bin_size_seconds)
    bin_ends_minutes = bins[1:] / 60

    # Adjust timestamps to be relative to the start of the window for binning
    periphery_counts, _ = np.histogram(periphery_crossings_in_window - start_time_seconds, bins=bins)
    
    return periphery_counts, bin_ends_minutes

def calculate_accumulated_periphery_crossings_in_window(animal_data, bin_size_seconds=150, start_time_seconds=3, end_time_seconds=603):
    """
    Calculates the accumulated number of periphery line crossings in each bin of a fixed time window.
    
    Args:
        animal_data (dict): The raw data for one animal, as loaded from its .mat file.
        bin_size_seconds (int): The size of each time bin in seconds.
        start_time_seconds (int): The start of the analysis window in seconds.
        end_time_seconds (int): The end of the analysis window in seconds.

    Returns:
        tuple: A tuple containing:
            - accumulated_periphery_counts (np.array): The accumulated number of periphery crossings in each bin.
            - bin_ends_minutes (np.array): The end of each time bin in minutes, for the x-axis.
    """
    periphery_counts, bin_ends_minutes = calculate_periphery_crossings_in_window(
        animal_data, bin_size_seconds, start_time_seconds, end_time_seconds
    )
    accumulated_periphery_counts = np.cumsum(periphery_counts)
    return accumulated_periphery_counts, bin_ends_minutes

def calculate_mean_thigmotaxis_by_sex(all_thigmotaxis_data):
    """
    Calculates the mean thigmotaxis index for all males and all females.

    Args:
        all_thigmotaxis_data (dict): A dictionary of thigmotaxis data for all animals.

    Returns:
        tuple: A tuple containing:
            - male_mean (np.array): The mean thigmotaxis index for males for each bin.
            - female_mean (np.array): The mean thigmotaxis index for females for each bin.
    """
    male_data = [data for animal_id, data in all_thigmotaxis_data.items() if animal_id.startswith('M')]
    female_data = [data for animal_id, data in all_thigmotaxis_data.items() if animal_id.startswith('F')]

    male_mean = np.mean(male_data, axis=0)
    female_mean = np.mean(female_data, axis=0)

    return male_mean, female_mean

def calculate_periphery_center_ratio(animal_data, start_time_seconds=3, end_time_seconds=603):
    """
    Calculates the ratio of periphery crossings to center crossings over a fixed time window.
    """
    all_crossings = animal_data['crossing_times'].flatten()
    periphery_crossings = animal_data['periphery_times'].flatten()

    time_window_mask = (all_crossings >= start_time_seconds) & (all_crossings < end_time_seconds)
    all_crossings_in_window = all_crossings[time_window_mask]

    periphery_mask = (periphery_crossings >= start_time_seconds) & (periphery_crossings < end_time_seconds)
    periphery_crossings_in_window = periphery_crossings[periphery_mask]
    
    total_crossings_count = len(all_crossings_in_window)
    periphery_crossings_count = len(periphery_crossings_in_window)
    
    center_crossings_count = max(total_crossings_count - periphery_crossings_count, 1)
    
    ratio = periphery_crossings_count / center_crossings_count
    
    return ratio

# --- Main Execution Block ---

if __name__ == '__main__':
    
    # 1. Load data
    raw_data = data_loader.load_matlab_data()
    loaded_data = {unit: data for unit, data in raw_data.items() if data is not None}

    if not loaded_data:
        print("Error: No data files were successfully loaded.")
    else:
        # 2. Define analysis parameters
        start_sec, end_sec = 3, 603
        bin_size = 150

        # 3. Run all analyses
        print("--- Running Analyses ---")
        analyzed_thigmotaxis = {}
        analyzed_freezing = {}
        analyzed_grooming = {}
        bin_centers = np.array([])

        for unit, data in loaded_data.items():
            # Thigmotaxis
            indices, bins = calculate_thigmotaxis_in_window(data, bin_size, start_sec, end_sec)
            analyzed_thigmotaxis[unit] = indices
            if bin_centers.size == 0 and bins.size > 0:
                bin_centers = bins
            # Freezing
            durations, _ = calculate_behavior_duration_in_window(data, 'Freezing_start_stop', bin_size, start_sec, end_sec)
            analyzed_freezing[unit] = durations
            # Grooming
            durations, _ = calculate_behavior_duration_in_window(data, 'grooming_start_stop', bin_size, start_sec, end_sec)
            analyzed_grooming[unit] = durations
        
        print("Analysis complete.")

        # 4. Generate plots using the plotting module
        print("\n--- Generating Plots ---")
        if analyzed_thigmotaxis and bin_centers.size > 0:
            behavioral_plotting.plot_thigmotaxis(analyzed_thigmotaxis, bin_centers)
        
