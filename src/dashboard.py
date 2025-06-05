import streamlit as st
import subprocess
import os
import glob
import time
from generate_individual_charts import generate_charts_for_config


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOCUSTFILE_PATH = os.path.join(PROJECT_ROOT, 'locustfile.py')
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
        with st.spinner("Running Locust test... This might take a while..."):
            process = subprocess.run(command, capture_output=True, text=True, check=True)
        st.success(f"Locust test completed for {api_or_test_case}!")
        # st.subheader("Locust Output:")
        # st.code(process.stdout)
        # if process.stderr:
        #     st.warning("Locust produced some warnings/errors:")
        #     st.code(process.stderr)
        st.write(f"Results saved!")
        generate_charts_for_config(output_dir)
        png_files = glob.glob(os.path.join(output_dir, "*.png"))
        if png_files:
            for png_file in png_files:
                st.image(png_file, caption=os.path.basename(png_file), use_container_width=True)
        else:
            st.info("No chart image was generated for this test run.")
        # st.markdown(f"**[Download Statistics CSV Report]({os.path.join(output_dir, 'report_stats.csv')})**")
        # st.markdown(f"**[Download Time Series CSV Report]({os.path.join(output_dir, 'report_stats_history.csv')})**")
    except subprocess.CalledProcessError as e:
        st.error(f"Locust test failed with exit code {e.returncode}:")
        st.code(e.stdout)
        st.code(e.stderr)
        if output_dir and os.path.exists(output_dir):
            st.warning(f"Partial results might be in: {output_dir}")
    except FileNotFoundError:
        st.error(f"Error: 'locust' command not found. Ensure Locust is installed and in your PATH.")
    except Exception as e:
        st.error(f"An unexpected error occurred during test execution: {e}")


# --- Streamlit UI ---
st.set_page_config(
    page_title="SarvamAI Transliteration API Performance Test Initiator",
    layout="centered", 
    initial_sidebar_state="auto"
)

st.title("🚀 SarvamAI Transliteration API Performance Test Initiator")

st.header("Configure and Trigger Test")

# Dropdown to select API or test case
api_options = {
    "Overall API Performance (All Languages)": "all_languages",
    # "Specific Language Model (Hindi)": "hindi_model",
    # "Specific Language Model (Malayalam)": "malayalam_model",
}
selected_api = st.selectbox("Select API / Test Case:", list(api_options.keys()))

users = st.number_input("Number of Users (Concurrency):", min_value=1, value=10, step=1)
spawn_rate = st.number_input("Spawn Rate (Users/sec):", min_value=1, value=2, step=1)
run_time_minutes = st.number_input("Run Time (Minutes):", min_value=1, value=1, step=1)

if st.button("Trigger Locust Test"):
    trigger_locust_test(users, spawn_rate, run_time_minutes, selected_api)

st.markdown("---")
st.caption("Simplified Performance Test Initiator powered by Streamlit & Locust")