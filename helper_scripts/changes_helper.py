from config import input_directory
import pandas as pd

from helper_scripts.Commit_date_helper import store_dates_for_files


# Reads what files have changed in which versions(s). Also calculates the time-ranges in which they changed.
def get_changes():
    component_chunks = pd.read_csv(input_directory + "/changes.csv", chunksize=5000)
    processed_chunks = []
    for component_chunk in component_chunks:
        processed_chunks.append(component_chunk)

    components = pd.concat(processed_chunks)
    store_dates_for_files(components[['version', 'name']])
    return components[['version', 'name', 'package']]
