import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_BASE_DIR = os.path.join(BASE_DIR, 'results')

def generate_charts_for_config(config_path):
    """
    Generates and saves language-wise p95 latency chart for a single configuration.
    """
    stats_csv_path = os.path.join(config_path, 'report_stats.csv')
    
    if not os.path.exists(stats_csv_path):
        print(f"Warning: {stats_csv_path} not found. Skipping chart generation for this config.")
        return

    df = pd.read_csv(stats_csv_path)

    # Filter out the 'Aggregated' row to focus on individual languages
    language_df = df[df['Name'] != 'Aggregated']

    if language_df.empty:
        print(f"No language-specific data found in {stats_csv_path}. Skipping chart.")
        return

    # Extract configuration name for chart title and filename
    config_name = os.path.basename(config_path)

    # --- Language-wise Latency Comparisons (p95) ---
    plt.figure(figsize=(12, 7))
    plt.bar(language_df['Name'], language_df['95%'], color='skyblue')
    plt.xlabel('Language')
    plt.ylabel('p95 Latency (ms)')
    plt.title(f'Language-wise p95 Latency for {config_name} Configuration')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    
    chart_filename = os.path.join(config_path, f'{config_name}_language_p95_latency.png')
    plt.savefig(chart_filename)
    plt.close()
    print(f"Generated: {chart_filename}")


def main():
    if not os.path.exists(RESULTS_BASE_DIR):
        print(f"Results directory not found at {RESULTS_BASE_DIR}. Please run load tests first.")
        return

    # Iterate through each configuration folder in the results directory
    config_folders = [f for f in os.listdir(RESULTS_BASE_DIR) if os.path.isdir(os.path.join(RESULTS_BASE_DIR, f))]
    
    if not config_folders:
        print(f"No configuration folders found in {RESULTS_BASE_DIR}. Please run load tests first.")
        return

    for folder_name in sorted(config_folders): # Sort for consistent order
        config_path = os.path.join(RESULTS_BASE_DIR, folder_name)
        generate_charts_for_config(config_path)

    print("\n--- All individual configuration charts generated! ---")

if __name__ == "__main__":
    main()