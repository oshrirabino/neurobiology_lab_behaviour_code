
"""
This module provides functions for plotting the analyzed experimental data.
Each function generates and saves a single plot.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# --- Plotting Helper Functions ---

def get_plot_color(animal_id):
    """Helper function to determine plot color based on animal ID."""
    sex = animal_id[0]
    color_code = animal_id[1]
    color_map = {
        'B': {'M': 'darkblue', 'F': 'cornflowerblue'},
        'R': {'M': 'darkred', 'F': 'lightcoral'},
        'G': {'M': 'darkgreen', 'F': 'limegreen'},
        'W': {'M': 'dimgray', 'F': 'silver'}
    }
    return color_map.get(color_code, {}).get(sex, 'black')

# --- Individual Plotting Functions (All 8 Animals) ---

def plot_thigmotaxis(all_animals_data, bin_ends_minutes):
    """
    Creates, saves, and shows a plot for Thigmotaxis Index for all animals.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for animal_id, indices in all_animals_data.items():
        color = get_plot_color(animal_id)
        is_female = animal_id.startswith('F')
        
        mfc = 'white' if is_female else color
        mec = 'black' if is_female else color

        ax.plot(bin_ends_minutes, indices, marker='o', linestyle='-', label=animal_id, color=color,
                markerfacecolor=mfc, markeredgecolor=mec, markersize=8, markeredgewidth=1.5)

    ax.set_title('Thigmotaxis Index Over a 10-Minute Window', fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Time (minutes)', fontsize=16)
    ax.set_ylabel('Thigmotaxis Index', fontsize=16)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 10.3)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray')
    ax.legend(title='Animal ID', loc='best', bbox_to_anchor=(0.2, 0.8), fontsize=12, title_fontsize=14)
    
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    if not os.path.exists('../plots'):
        os.makedirs('../plots')
    plt.savefig('../plots/thigmotaxis_over_time_10min.png', dpi=300)
    print("Plot saved to 'plots/thigmotaxis_over_time_10min.png'")
    plt.show()

# --- Grouped Comparison Plotting Functions (Male vs Female) ---

def draw_total_crossings_on_ax(ax, data_male, data_female, bin_ends_minutes, group_name):
    """
    Draws total line crossings for a male/female pair on a given Axes object (bar chart).
    """
    group_code_char = group_name[0]
    male_id = f'M{group_code_char}' 
    female_id = f'F{group_code_char}'
    
    color_male = get_plot_color(male_id)
    color_female = get_plot_color(female_id)

    bar_width = 0.8
    x = np.arange(len(bin_ends_minutes))

    ax.bar(bin_ends_minutes - bar_width/2, data_male, bar_width, label=f'Male', color=color_male)
    ax.bar(bin_ends_minutes + bar_width/2, data_female, bar_width, label=f'Female', color=color_female)

    ax.set_title(f'Total Crossings: {group_name} Group', fontsize=18, fontweight='bold')
    ax.set_xlabel('Time (minutes)', fontsize=14)
    ax.set_ylabel('Total Crossings', fontsize=14)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 11)
    
    max_y = max(np.max(data_male) if data_male.size > 0 else 0, np.max(data_female) if data_female.size > 0 else 0)
    ax.set_ylim(0, max_y * 1.15 if max_y > 0 else 10)
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray', axis='y')
    ax.legend(fontsize=12)

def plot_total_crossings_by_group(all_crossings_data, bin_ends_minutes):
    """
    Creates, saves, and shows serial plots of total crossings, one for each color group.
    """
    print("\n--- Generating Total Crossings Plots (by Group) ---")
    color_groups = ['B', 'R', 'G', 'W']
    group_names = {'B': 'Blue', 'R': 'Red', 'G': 'Green', 'W': 'White'}

    for group_code in color_groups:
        fig, ax = plt.subplots(figsize=(10, 7))
        male_id = f'M{group_code}'
        female_id = f'F{group_code}'
        
        male_crossings = all_crossings_data.get(male_id, np.zeros(len(bin_ends_minutes)))
        female_crossings = all_crossings_data.get(female_id, np.zeros(len(bin_ends_minutes)))
        
        group_name = group_names[group_code]
        draw_total_crossings_on_ax(ax, male_crossings, female_crossings, bin_ends_minutes, group_name)
        
        fig.tight_layout()
        filename = f'../plots/total_crossings/total_crossings_group_{group_name.lower()}.png'
        if not os.path.exists('../plots/total_crossings'):
            os.makedirs('../plots/total_crossings', exist_ok=True)
        plt.savefig(filename, dpi=300)
        print(f"Plot saved to '{filename}'")
        plt.show()

def draw_thigmotaxis_on_ax(ax, data_male, data_female, bin_ends_minutes, group_name):
    """
    Draws thigmotaxis index for a male/female pair on a given Axes object (bar chart).
    """
    group_code_char = group_name[0]
    male_id = f'M{group_code_char}' 
    female_id = f'F{group_code_char}'
    
    color_male = get_plot_color(male_id)
    color_female = get_plot_color(female_id)

    bar_width = 0.8
    x = np.arange(len(bin_ends_minutes))

    ax.bar(bin_ends_minutes - bar_width/2, data_male, bar_width, label=f'Male', color=color_male)
    ax.bar(bin_ends_minutes + bar_width/2, data_female, bar_width, label=f'Female', color=color_female)

    ax.set_title(f'Thigmotaxis Index: {group_name} Group', fontsize=18, fontweight='bold')
    ax.set_xlabel('Time (minutes)', fontsize=14)
    ax.set_ylabel('Thigmotaxis Index', fontsize=14)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 11)
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray', axis='y')
    ax.legend(fontsize=12)

def plot_thigmotaxis_by_group(all_thigmotaxis_data, bin_ends_minutes):
    """
    Creates, saves, and shows serial plots of thigmotaxis index, one for each color group.
    """
    print("\n--- Generating Thigmotaxis Index Plots (by Group) ---")
    color_groups = ['B', 'R', 'G', 'W']
    group_names = {'B': 'Blue', 'R': 'Red', 'G': 'Green', 'W': 'White'}

    for group_code in color_groups:
        fig, ax = plt.subplots(figsize=(10, 7))
        male_id = f'M{group_code}'
        female_id = f'F{group_code}'
        
        male_data = all_thigmotaxis_data.get(male_id, np.zeros(len(bin_ends_minutes)))
        female_data = all_thigmotaxis_data.get(female_id, np.zeros(len(bin_ends_minutes)))
        
        group_name = group_names[group_code]
        draw_thigmotaxis_on_ax(ax, male_data, female_data, bin_ends_minutes, group_name)

        fig.tight_layout()
        filename = f'../plots/thigmotaxis/thigmotaxis_group_{group_name.lower()}.png'
        if not os.path.exists('../plots/thigmotaxis'):
            os.makedirs('../plots/thigmotaxis', exist_ok=True)
        plt.savefig(filename, dpi=300)
        print(f"Plot saved to '{filename}'")
        plt.show()

def draw_freezing_grooming_on_ax(ax, data_male_f, data_female_f, data_male_g, data_female_g, bin_ends_minutes, group_name):
    """
    Draws a 4-bar grouped chart for freezing and grooming durations for a male/female pair.
    """
    group_code_char = group_name[0]
    male_id = f'M{group_code_char}'
    female_id = f'F{group_code_char}'
    
    color_male = get_plot_color(male_id)
    color_female = get_plot_color(female_id)

    bar_width = 0.5
    x = bin_ends_minutes

    ax.bar(x - 1.5*bar_width, data_male_f, bar_width, label='Male Freezing', color=color_male, hatch='//')
    ax.bar(x - 0.5*bar_width, data_female_f, bar_width, label='Female Freezing', color=color_female, hatch='//')
    ax.bar(x + 0.5*bar_width, data_male_g, bar_width, label='Male Grooming', color=color_male)
    ax.bar(x + 1.5*bar_width, data_female_g, bar_width, label='Female Grooming', color=color_female)

    ax.set_title(f'Freezing & Grooming: {group_name} Group', fontsize=18, fontweight='bold')
    ax.set_xlabel('Time (minutes)', fontsize=14)
    ax.set_ylabel('Duration (seconds)', fontsize=14)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 11.5)
    
    all_data = np.concatenate([data_male_f, data_female_f, data_male_g, data_female_g])
    max_y = np.max(all_data) if all_data.size > 0 else 0
    ax.set_ylim(0, max_y * 1.15 if max_y > 0 else 10)

    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray', axis='y')
    ax.legend(fontsize=12)

def plot_freezing_grooming_by_group(all_freezing_data, all_grooming_data, bin_ends_minutes):
    """
    Creates, saves, and shows serial plots of freezing & grooming, one for each color group.
    """
    print("\n--- Generating Freezing & Grooming Plots (by Group) ---")
    color_groups = ['B', 'R', 'G', 'W']
    group_names = {'B': 'Blue', 'R': 'Red', 'G': 'Green', 'W': 'White'}

    for group_code in color_groups:
        fig, ax = plt.subplots(figsize=(10, 7))
        male_id = f'M{group_code}'
        female_id = f'F{group_code}'
        
        male_f_data = all_freezing_data.get(male_id, np.zeros(len(bin_ends_minutes)))
        female_f_data = all_freezing_data.get(female_id, np.zeros(len(bin_ends_minutes)))
        male_g_data = all_grooming_data.get(male_id, np.zeros(len(bin_ends_minutes)))
        female_g_data = all_grooming_data.get(female_id, np.zeros(len(bin_ends_minutes)))
        
        group_name = group_names[group_code]
        draw_freezing_grooming_on_ax(ax, male_f_data, female_f_data, male_g_data, female_g_data, bin_ends_minutes, group_name)

        fig.tight_layout()
        filename = f'../plots/freezing_grooming/freezing_grooming_group_{group_name.lower()}.png'
        if not os.path.exists('../plots/freezing_grooming'):
            os.makedirs('../plots/freezing_grooming', exist_ok=True)
        plt.savefig(filename, dpi=300)
        print(f"Plot saved to '{filename}'")
        plt.show()

def plot_freezing_grooming_all_animals(all_freezing_data, all_grooming_data, bin_ends_minutes):
    """
    Creates, saves, and shows a plot for freezing and grooming durations for all animals.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    animal_ids = sorted(all_freezing_data.keys())

    for animal_id in animal_ids:
        color = get_plot_color(animal_id)
        is_female = animal_id.startswith('F')
        
        mfc = 'white' if is_female else color
        mec = 'black' if is_female else color

        # Plot freezing (solid line, circle marker)
        ax.plot(bin_ends_minutes, all_freezing_data[animal_id], marker='o', linestyle='-', color=color,
                markerfacecolor=mfc, markeredgecolor=mec, markersize=8, markeredgewidth=1.5)
        
        # Plot grooming (dashed line, x marker)
        ax.plot(bin_ends_minutes, all_grooming_data[animal_id], marker='x', linestyle='--', color=color,
                markersize=8, markeredgewidth=1.5)

    ax.set_title('Freezing and Grooming Over Time', fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Time (minutes)', fontsize=16)
    ax.set_ylabel('Duration (seconds)', fontsize=16)
    
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='gray', linestyle='-', marker='o', label='Freezing'),
        Line2D([0], [0], color='gray', linestyle='--', marker='x', label='Grooming'),
        Line2D([0], [0], color='w', label='') # Spacer
    ]

    for animal_id in animal_ids:
        color = get_plot_color(animal_id)
        is_female = animal_id.startswith('F')
        mfc = 'white' if is_female else color
        mec = 'black' if is_female else color
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label=animal_id,
                                     markerfacecolor=mfc, markeredgecolor=mec, markersize=10))

    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))

    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 10.3)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray')

    max_y_f = np.max([np.max(d) for d in all_freezing_data.values() if d.size > 0]) if all_freezing_data else 0
    max_y_g = np.max([np.max(d) for d in all_grooming_data.values() if d.size > 0]) if all_grooming_data else 0
    ax.set_ylim(0, max(max_y_f, max_y_g) * 1.15 if max(max_y_f, max_y_g) > 0 else 10)

    fig.tight_layout()

    output_dir = '../plots/freezing_grooming'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    filename = f'{output_dir}/freezing_grooming_all.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved to '{filename}'")
    plt.show()
    plt.close(fig)

def plot_accumulated_crossings_all_animals(all_animals_data, bin_ends_minutes):
    """
    Creates, saves, and shows a plot for accumulated crossings for all animals.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for animal_id, accumulated_data in all_animals_data.items():
        color = get_plot_color(animal_id)
        is_female = animal_id.startswith('F')
        
        mfc = 'white' if is_female else color
        mec = 'black' if is_female else color

        ax.plot(bin_ends_minutes, accumulated_data, marker='o', linestyle='-', label=animal_id, color=color,
                markerfacecolor=mfc, markeredgecolor=mec, markersize=8, markeredgewidth=1.5)

    ax.set_title('Accumulated Crossings Over a 10-Minute Window', fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Time (minutes)', fontsize=16)
    ax.set_ylabel('Accumulated Crossings', fontsize=16)
    
    max_y = np.max([np.max(d) for d in all_animals_data.values() if d.size > 0]) if all_animals_data else 0
    ax.set_ylim(0, max_y * 1.1 if max_y > 0 else 10)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 10.3)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray')
    ax.legend(title='Animal ID', loc='best', bbox_to_anchor=(0.2, 0.8), fontsize=12, title_fontsize=14)
    
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    output_dir = '../plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f'{output_dir}/accumulated_crossings_all.png'
    plt.savefig(filename, dpi=300)
    print(f"Plot saved to '{filename}'")
    plt.show()
    plt.close(fig)

def plot_total_crossings_all_animals(all_animals_data, bin_ends_minutes):
    """
    Creates, saves, and shows a plot for total crossings for all animals.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for animal_id, total_data in all_animals_data.items():
        color = get_plot_color(animal_id)
        is_female = animal_id.startswith('F')
        
        mfc = 'white' if is_female else color
        mec = 'black' if is_female else color

        ax.plot(bin_ends_minutes, total_data, marker='o', linestyle='-', label=animal_id, color=color,
                markerfacecolor=mfc, markeredgecolor=mec, markersize=8, markeredgewidth=1.5)

    ax.set_title('Open Field - Total Locomotor Activity', fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Time (minutes)', fontsize=16)
    ax.set_ylabel('Total Crossings', fontsize=16)
    
    max_y = np.max([np.max(d) for d in all_animals_data.values() if d.size > 0]) if all_animals_data else 0
    ax.set_ylim(0, max_y * 1.1 if max_y > 0 else 10)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 10.3)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray')
    ax.legend(title='Animal ID', loc='best', bbox_to_anchor=(0.2, 0.8), fontsize=12, title_fontsize=14)
    
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    output_dir = '../plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f'{output_dir}/total_crossings_all.png'
    plt.savefig(filename, dpi=300)
    print(f"Plot saved to '{filename}'")
    plt.show()
    plt.close(fig)

def plot_accumulated_periphery_crossings_all_animals(all_animals_data, bin_ends_minutes):
    """
    Creates, saves, and shows a plot for accumulated periphery crossings for all animals.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for animal_id, accumulated_data in all_animals_data.items():
        color = get_plot_color(animal_id)
        is_female = animal_id.startswith('F')
        
        mfc = 'white' if is_female else color
        mec = 'black' if is_female else color

        ax.plot(bin_ends_minutes, accumulated_data, marker='o', linestyle='-', label=animal_id, color=color,
                markerfacecolor=mfc, markeredgecolor=mec, markersize=8, markeredgewidth=1.5)

    ax.set_title('Accumulated Periphery Crossings Over a 10-Minute Window', fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Time (minutes)', fontsize=16)
    ax.set_ylabel('Accumulated Periphery Crossings', fontsize=16)
    
    max_y = np.max([np.max(d) for d in all_animals_data.values() if d.size > 0]) if all_animals_data else 0
    ax.set_ylim(0, max_y * 1.1 if max_y > 0 else 10)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 10.3)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray')
    ax.legend(title='Animal ID', loc='best', bbox_to_anchor=(0.2, 0.8), fontsize=12, title_fontsize=14)
    
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    output_dir = '../plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f'{output_dir}/accumulated_periphery_crossings_all.png'
    plt.savefig(filename, dpi=300)
    print(f"Plot saved to '{filename}'")
    plt.show()
    plt.close(fig)

def plot_mean_thigmotaxis_by_sex(male_mean, female_mean, bin_ends_minutes):
    """
    Creates, saves, and shows a bar chart comparing the mean thigmotaxis index
    between all males and all females.
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    bar_width = 0.8
    x = np.arange(len(bin_ends_minutes))

    ax.bar(bin_ends_minutes - bar_width/2, male_mean, bar_width, label='Male Mean', color='orange')
    ax.bar(bin_ends_minutes + bar_width/2, female_mean, bar_width, label='Female Mean', color='yellow')

    ax.set_title('Mean Thigmotaxis Index: All Males vs. All Females', fontsize=18, fontweight='bold')
    ax.set_xlabel('Time (minutes)', fontsize=14)
    ax.set_ylabel('Mean Thigmotaxis Index', fontsize=14)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(np.arange(0, 10.1, 2.5))
    ax.set_xlim(0, 11)
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray', axis='y')
    ax.legend(fontsize=12)

    fig.tight_layout()

    output_dir = '../plots/thigmotaxis'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    filename = f'{output_dir}/thigmotaxis_mean_by_sex.png'
    plt.savefig(filename, dpi=300)
    print(f"Plot saved to '{filename}'")
    plt.show()
    plt.close(fig)


def plot_mean_periphery_center_ratio_by_sex(all_animals_ratios):
    """
    Creates a bar chart comparing mean periphery/center ratio by sex, with individual data points.
    """
    print("\n--- Generating Mean Periphery/Center Ratio by Sex Plot ---")
    
    male_ratios = []
    female_ratios = []
    male_ids = []
    female_ids = []

    for animal_id, ratio in all_animals_ratios.items():
        if animal_id.startswith('M'):
            male_ratios.append(ratio)
            male_ids.append(animal_id)
        elif animal_id.startswith('F'):
            female_ratios.append(ratio)
            female_ids.append(animal_id)

    if not male_ratios or not female_ratios:
        print("Warning: Not enough data to compare sexes.")
        return

    mean_male = np.mean(male_ratios)
    mean_female = np.mean(female_ratios)
    sem_male = np.std(male_ratios, ddof=1) / np.sqrt(len(male_ratios))
    sem_female = np.std(female_ratios, ddof=1) / np.sqrt(len(female_ratios))

    fig, ax = plt.subplots(figsize=(8, 7))

    # Bar plot
    bar_positions = [0, 1]
    bar_labels = ['Male', 'Female']
    means = [mean_male, mean_female]
    sems = [sem_male, sem_female]
    ax.bar(bar_positions, means, yerr=sems, capsize=5, color=['orange', 'yellow'], width=0.6)

    # Individual data points (scatter plot)
    jitter = 0.05
    male_x = np.random.normal(0, jitter, len(male_ratios))
    female_x = np.random.normal(1, jitter, len(female_ratios))

    ax.scatter(male_x, male_ratios, color=[get_plot_color(id) for id in male_ids], zorder=2, label='_nolegend_')
    
    # Female points hollow
    female_colors = [get_plot_color(id) for id in female_ids]
    ax.scatter(female_x, female_ratios, facecolors='white',
               edgecolors=female_colors, s=60, zorder=2, label='_nolegend_') # s is marker size

    ax.set_title('Mean Periphery/Center Ratio by Sex', fontsize=18, fontweight='bold', pad=20)
    ax.set_ylabel('Periphery/Center Ratio', fontsize=14)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, fontsize=12)
    
    max_y = max(np.max(male_ratios) if male_ratios else 0, np.max(female_ratios) if female_ratios else 0)
    ax.set_ylim(0, max_y * 1.15 if max_y > 0 else 1)
    ax.grid(which='major', linestyle='--', linewidth='0.5', color='gray', axis='y')

    # Custom legend for groups
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=f'{id} (M)', markerfacecolor=get_plot_color(id), markersize=8) for id in sorted(male_ids)]
    legend_elements += [Line2D([0], [0], marker='o', color='w', label=f'{id} (F)', markerfacecolor='white',
                               markeredgecolor=get_plot_color(id), markersize=8) for id in sorted(female_ids)]
    ax.legend(handles=legend_elements, title='Animals', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12, title_fontsize=14)

    fig.tight_layout(rect=[0, 0, 0.85, 1])
    
    output_dir = '../plots/thigmotaxis'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    filename = f'{output_dir}/mean_periphery_center_ratio_by_sex.png'
    plt.savefig(filename, dpi=300)
    print(f"Plot saved to '{filename}'")
    plt.show()
    plt.close(fig)

