import subprocess
import os
import time
import shutil
import math


concurrency = [1, 5, 10, 25]
spawn_rate = [1, 2, 2, 4]
run_time = ["1m", "1m", "3m", "5m"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCUSTFILE_PATH = os.path.join(BASE_DIR, 'sarvamai_benchmarking.py')
RESULTS_DIR = os.path.join(BASE_DIR, "..", 'results')

def run_locust_test(num_users, spawn_rate_val, run_time_val):
    dir_name = f"c{num_users}_s{spawn_rate_val}_rt{run_time_val}"
    output_dir = os.path.join(RESULTS_DIR, dir_name)

    os.makedirs(output_dir, exist_ok=True)
    print(f"\n--- Starting test: Concurrency={num_users}, Spawn Rate={spawn_rate_val}, Run Time={run_time_val} ---")
    print(f"Results will be saved to: {output_dir}")
    
    command = [
        "locust",
        "-f", LOCUSTFILE_PATH,
        "--headless",
        "-u", str(num_users),
        "-r", str(spawn_rate_val),
        "--run-time", run_time_val,
        f"--csv={os.path.join(output_dir, 'report')}"
    ]

    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Locust test completed successfully.")
        print("STDOUT:\n", process.stdout)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print(f"--- Test for {dir_name} finished. ---\n\n")
    time.sleep(120)

def main():
    start_time = time.time()
    if os.path.exists(RESULTS_DIR):
        print(f"Clearing existing results directory: {RESULTS_DIR}")
        shutil.rmtree(RESULTS_DIR)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print(f"Created main results directory: {RESULTS_DIR}")

    if not os.getenv("SARVAM_API_KEY"):
        print("\nERROR: SARVAM_API_KEY environment variable is not set.")
        print("Please set it before running this script (e.g., export SARVAM_API_KEY='YOUR_KEY').")
        return

    for i in range(4):
        num_users = concurrency[i]
        spawn_rate_val = spawn_rate[i]
        run_time_val = run_time[i]
        run_locust_test(num_users, spawn_rate_val, run_time_val)
        
    end_time = time.time()
    
    total_seconds = end_time - start_time
    minutes = math.floor(total_seconds / 60)
    seconds = total_seconds % 60

    print("\n--- All load tests completed! ---")
    print(f"\n--- Total time taken: {minutes:.0f} minutes and {seconds:.2f} seconds ---")
    print(f"Results are saved in the '{os.path.basename(RESULTS_DIR)}' directory.")

if __name__ == "__main__":
    main()