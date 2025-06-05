import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_BASE_DIR = os.path.join(BASE_DIR, 'results')
OVERALL_CHARTS_DIR = os.path.join(RESULTS_BASE_DIR, 'overall_charts')


def collect_data_from_all_configs():
    """
    Collects p50, p75, p95 latency and average response time for the 'Aggregated'
    row from all test configurations.
    """
    all_data = []
    
    if not os.path.exists(RESULTS_BASE_DIR):
        print(f"Results directory not found at {RESULTS_BASE_DIR}.")
        return pd.DataFrame()

    config_folders = [f for f in os.listdir(RESULTS_BASE_DIR) if os.path.isdir(os.path.join(RESULTS_BASE_DIR, f)) and f != 'overall_charts']

    if not config_folders:
        print(f"No configuration folders found in {RESULTS_BASE_DIR}.")
        return pd.DataFrame()

    for folder_name in sorted(config_folders): # Ensure consistent order
        config_path = os.path.join(RESULTS_BASE_DIR, folder_name)
        stats_csv_path = os.path.join(config_path, 'report_stats.csv')

        if not os.path.exists(stats_csv_path):
            print(f"Warning: {stats_csv_path} not found. Skipping data collection for {folder_name}.")
            continue

        df = pd.read_csv(stats_csv_path)
        
        # Get the 'Aggregated' row, which summarizes overall performance
        # Check if 'Aggregated' row exists before trying to access it
        if 'Aggregated' in df['Name'].values:
            aggregated_row = df[df['Name'] == 'Aggregated'].iloc[0]
        else:
            print(f"Warning: 'Aggregated' row not found in {stats_csv_path}. Skipping data for {folder_name}.")
            continue

        # Extract relevant metrics
        # Ensure 'Request Count' is not zero before division to avoid ZeroDivisionError
        request_count = aggregated_row['Request Count']
        failure_count = aggregated_row['Failure Count']
        error_rate = (failure_count / request_count) * 100 if request_count > 0 else 0

        data_point = {
            'Configuration': folder_name,
            'p50 Latency': aggregated_row['50%'],
            'p75 Latency': aggregated_row['75%'],
            'p95 Latency': aggregated_row['95%'],
            'Average Response Time': aggregated_row['Average Response Time'],
            'Requests/s': aggregated_row['Requests/s'],
            'Error Rate': error_rate
        }
        all_data.append(data_point)

    return pd.DataFrame(all_data)

def main():
    df_overall = collect_data_from_all_configs()

    if df_overall.empty:
        print("No data collected for overall comparison. Exiting.")
        return

    os.makedirs(OVERALL_CHARTS_DIR, exist_ok=True)
    print(f"Saving overall comparison charts to: {OVERALL_CHARTS_DIR}")

    # --- Bar/line chart for p95, p75, p50 latency across configurations ---
    plt.figure(figsize=(14, 8))
    ax = plt.gca() # Get current axes to use for plotting

    df_overall.set_index('Configuration')[['p50 Latency', 'p75 Latency', 'p95 Latency']].plot(
        kind='bar', figsize=(14, 8), colormap='viridis', ax=ax # Pass ax to plot on it
    )
    plt.xlabel('Configuration')
    plt.ylabel('Latency (ms)')
    plt.title('p50, p75, p95 Latency Across Configurations (Aggregated)')
    
    # Correct way to rotate and align x-axis labels after plotting with pandas
    # This applies to the current axes (ax)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right') # This is the correct way
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OVERALL_CHARTS_DIR, 'overall_latency_comparison.png'))
    plt.close()
    print(f"Generated: {os.path.join(OVERALL_CHARTS_DIR, 'overall_latency_comparison.png')}")

    # --- Optional: RPS and Error Rate across configurations ---
    fig, ax1 = plt.subplots(figsize=(14, 8))

    color = 'tab:blue'
    ax1.set_xlabel('Configuration')
    ax1.set_ylabel('Requests/s', color=color)
    ax1.plot(df_overall['Configuration'], df_overall['Requests/s'], marker='o', color=color, label='Requests/s')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Correct way to set x-axis label properties for ax1
    ax1.tick_params(axis='x', labelrotation=45) # Use labelrotation
    plt.setp(ax1.get_xticklabels(), ha='right') # And then set horizontal alignment separately if needed
    
    ax1.set_title('RPS and Error Rate Across Configurations')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    ax2 = ax1.twinx() # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Error Rate (%)', color=color)
    ax2.plot(df_overall['Configuration'], df_overall['Error Rate'], marker='x', linestyle='--', color=color, label='Error Rate (%)')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(bottom=0) # Ensure error rate starts from 0

    fig.tight_layout() # otherwise the right y-label is slightly clipped
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9)) # Place legend
    plt.savefig(os.path.join(OVERALL_CHARTS_DIR, 'overall_rps_error_rate.png'))
    plt.close()
    print(f"Generated: {os.path.join(OVERALL_CHARTS_DIR, 'overall_rps_error_rate.png')}")


    print("\n--- All overall comparison charts generated! ---")

if __name__ == "__main__":
    main()