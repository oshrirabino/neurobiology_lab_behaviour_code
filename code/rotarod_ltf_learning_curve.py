import os
import matplotlib.pyplot as plt
import numpy as np
import data_loader
import behavioral_plotting as plotting

# Create output directory
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PLOT_DIR = os.path.join(PROJECT_ROOT, 'plots', 'rotarod')
os.makedirs(PLOT_DIR, exist_ok=True)


def plot_individual_learning_curves(rotarod_df):
    """
    Plot learning curves for all individual testers.
    
    Args:
        rotarod_df: DataFrame from load_rotarod_data()
    """
    plt.figure(figsize=(10, 6))
    
    # Get unique subjects
    subjects = rotarod_df['Subject_ID'].unique()
    
    # Plot each subject's learning curve
    for subject in subjects:
        subject_data = rotarod_df[rotarod_df['Subject_ID'] == subject]
        
        # Get color for this subject
        color = plotting.get_plot_color(subject)
        is_female = subject.startswith('F')
        
        mfc = 'white' if is_female else color
        mec = 'black' if is_female else color
        
        # Plot the learning curve
        plt.plot(subject_data['Session'], 
                subject_data['Latency_to_Fall'], 
                marker='o', 
                label=subject, 
                color=color,
                linewidth=2,
                markersize=8, # Increased markersize for visibility
                markerfacecolor=mfc,
                markeredgecolor=mec,
                markeredgewidth=1.5)
    
    plt.xlabel('Session Number', fontsize=14)
    plt.ylabel('Latency to Fall (seconds)', fontsize=14)
    plt.title('Rotarod Learning Curves - All Subjects', fontsize=18, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.xticks(np.arange(1, 6, 1))  # Set integer ticks
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(PLOT_DIR, 'all_subjects_learning_curves.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved individual learning curves to: {output_path}")
    plt.close()


def plot_sex_comparison(rotarod_df):
    """
    Plot mean learning curves comparing males and females.
    
    Args:
        rotarod_df: DataFrame from load_rotarod_data()
    """
    # Extract sex from Subject_ID (first letter: F or M)
    rotarod_df['Sex'] = rotarod_df['Subject_ID'].astype(str).str[0]
    
    # Separate by sex
    males = rotarod_df[rotarod_df['Sex'] == 'M']
    females = rotarod_df[rotarod_df['Sex'] == 'F']
    
    # Calculate mean and SEM for each session
    male_means = males.groupby('Session')['Latency_to_Fall'].mean()
    male_sem = males.groupby('Session')['Latency_to_Fall'].sem()
    
    female_means = females.groupby('Session')['Latency_to_Fall'].mean()
    female_sem = females.groupby('Session')['Latency_to_Fall'].sem()
    
    plt.figure(figsize=(10, 6))
    
    # Plot males (orange)
    sessions = male_means.index
    plt.plot(sessions, male_means, marker='o', color='orange', 
             linewidth=3, markersize=8, label='Males')
    plt.fill_between(sessions, 
                     male_means - male_sem, 
                     male_means + male_sem, 
                     color='orange', alpha=0.2)
    
    # Plot females (yellow)
    sessions = female_means.index
    plt.plot(sessions, female_means, marker='o', color='yellow', 
             linewidth=3, markersize=8, label='Females', 
             markeredgecolor='black', markeredgewidth=1)
    plt.fill_between(sessions, 
                     female_means - female_sem, 
                     female_means + female_sem, 
                     color='yellow', alpha=0.2)
    
    plt.xlabel('Session Number', fontsize=14)
    plt.ylabel('Mean Latency to Fall (seconds)', fontsize=14)
    plt.title('Rotarod Learning Curves - Sex Comparison', fontsize=18, fontweight='bold')
    plt.legend(fontsize=12)
    plt.xticks(np.arange(1, 6, 1))  # Set integer ticks
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(PLOT_DIR, 'sex_comparison_learning_curves.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved sex comparison plot to: {output_path}")
    plt.close()
    
    # Print summary statistics
    print("\n" + "="*50)
    print("Summary Statistics")
    print("="*50)
    print(f"Males: n={len(males['Subject_ID'].unique())}")
    print(f"Females: n={len(females['Subject_ID'].unique())}")
    print("\nMean latency to fall by session:")
    print("\nMales:")
    print(male_means)
    print("\nFemales:")
    print(female_means)


if __name__ == '__main__':
    # Load rotarod data
    print("Loading rotarod data...")
    rotarod_df = data_loader.load_rotarod_data()
    
    if rotarod_df is not None:
        print(f"\nLoaded {len(rotarod_df)} trials from {rotarod_df['Subject_ID'].nunique()} subjects")
        
        # Plot individual learning curves
        print("\nGenerating individual learning curves plot...")
        plot_individual_learning_curves(rotarod_df)
        
        # Plot sex comparison
        print("\nGenerating sex comparison plot...")
        plot_sex_comparison(rotarod_df)
        
        print("\nAll plots saved successfully!")
    else:
        print("Failed to load rotarod data.")