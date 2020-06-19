
from config import initialize_config

# Reads settings from command line

initialize_config()

from dynamic_Warp import generate_dtw_analysis_files
from MBA import generate_mba_analysis_files
from Exploration import run_exploration

# generate_dtw_analysis_files()

# generate_mba_analysis_files()

# Start the exploration
run_exploration()
