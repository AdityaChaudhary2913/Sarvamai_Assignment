import streamlit as st
import subprocess
import os
import glob
import time
from generate_individual_charts import generate_charts_for_config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOCUSTFILE_PATH = os.path.join(PROJECT_ROOT, 'sarvamai_benchmarking.py')
RESULTS_BASE_DIR = os.path.join(PROJECT_ROOT, '..', 'results')

def trigger_locust_test(users, spawn_rate, run_time_minutes, api_or_test_case):
    st.info(f"Starting test for: {api_or_test_case} with {users} users, {spawn_rate} spawn rate, {run_time_minutes} min run time.")

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    config_name = f"c{users}_s{spawn_rate}_rt{run_time_minutes}m_{timestamp}"
    output_dir = os.path.join(RESULTS_BASE_DIR, config_name)
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "locust",
        "-f", LOCUSTFILE_PATH,
        "--headless",
        "-u", str(users),
        "-r", str(spawn_rate),
        "--run-time", f"{run_time_minutes}m",
        "--csv", os.path.join(output_dir, "report"),
    ]

    st.write(f"Executing command: `{' '.join(command)}`")

    process = None
    try:
        with st.spinner(f"Running Locust test for {config_name}... This might take a while..."):
            process = subprocess.run(command, capture_output=True, text=True, check=True)
        st.success(f"Locust test completed for {config_name}!")
        st.write(f"Results saved to: `{output_dir}`")
        generate_charts_for_config(output_dir)
        png_files = glob.glob(os.path.join(output_dir, "*.png"))
        if png_files:
            for png_file in png_files:
                st.image(png_file, caption=os.path.basename(png_file), use_container_width=True)
        else:
            st.info("No chart image was generated for this test run.")
    except subprocess.CalledProcessError as e:
        st.error(f"Locust test failed for {config_name} with exit code {e.returncode}:")
        st.code(e.stdout)
        st.code(e.stderr)
        if output_dir and os.path.exists(output_dir):
            st.warning(f"Partial results might be in: {output_dir}")
    except FileNotFoundError:
        st.error(f"Error: 'locust' command not found. Ensure Locust is installed and in your PATH.")
    except Exception as e:
        st.error(f"An unexpected error occurred during test execution for {config_name}: {e}")

## Streamlit UI
st.set_page_config(
    page_title="SarvamAI Transliteration API Performance Test Initiator",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🚀 SarvamAI Transliteration API Performance Test Initiator")

st.header("Configure and Trigger Multiple Tests")

# Initialize session state for test configurations if not already present
if 'test_configs' not in st.session_state:
    st.session_state.test_configs = []

# Dropdown to select API or test case (applies to all configurations for simplicity here)
api_options = {
    "Overall API Performance (All Languages)": "all_languages",
}
selected_api = st.selectbox("Select API / Test Case for all configurations:", list(api_options.keys()))

st.subheader("Add Test Configurations")

# Button to add a new configuration
if st.button("Add New Test Configuration"):
    st.session_state.test_configs.append({
        "users": 10,
        "spawn_rate": 2,
        "run_time_minutes": 1
    })

# Display and edit existing configurations
if st.session_state.test_configs:
    st.markdown("---")
    st.subheader("Current Test Configurations:")
    for i, config in enumerate(st.session_state.test_configs):
        st.markdown(f"**Configuration {i+1}**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.session_state.test_configs[i]["users"] = st.number_input(
                f"Users {i+1}:", min_value=1, value=config["users"], step=1, key=f"users_{i}"
            )
        with col2:
            st.session_state.test_configs[i]["spawn_rate"] = st.number_input(
                f"Spawn Rate {i+1}:", min_value=1, value=config["spawn_rate"], step=1, key=f"spawn_rate_{i}"
            )
        with col3:
            st.session_state.test_configs[i]["run_time_minutes"] = st.number_input(
                f"Run Time (min) {i+1}:", min_value=1, value=config["run_time_minutes"], step=1, key=f"run_time_{i}"
            )
        with col4:
            if st.button(f"Remove {i+1}", key=f"remove_config_{i}"):
                st.session_state.test_configs.pop(i)
                st.rerun() # Rerun to update the list immediately
        st.markdown("---")

if st.session_state.test_configs:
    if st.button("Trigger All Locust Tests"):
        st.header("Starting All Configured Tests")
        for i, config in enumerate(st.session_state.test_configs):
            st.markdown(f"## Running Test Configuration {i+1}")
            trigger_locust_test(
                config["users"],
                config["spawn_rate"],
                config["run_time_minutes"],
                selected_api
            )
            st.success(f"Finished Configuration {i+1}")
            st.markdown("---")
        st.balloons()
        st.success("All configured tests have been completed!")
else:
    st.info("No test configurations added yet. Click 'Add New Test Configuration' to get started.")

st.markdown("---")
st.caption("Simplified Performance Test Initiator powered by Streamlit & Locust")