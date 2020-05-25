import pandas as pd
from config import input_directory
from helper_scripts import Commit_date_helper
from helper_scripts.Commit_date_helper import store_dates_for_files


def get_components():

    component_chunks = pd.read_csv(input_directory + "/component-characteristics-consecOnly.csv", chunksize=5000)
    # Create an empty copy with the same headers
    class_components = None
    processed_chunks = []
    # For each chunk, apply the inner class filter and append the result to class_components.
    for component_chunk in component_chunks:
        # only consider classes, not packages
        class_chunk_components = component_chunk[component_chunk['type'] == 'class']
        # Define the inner class filter
        mask = ~class_chunk_components['name'].str.contains("$", regex=False)
        # Apply the filter operation
        class_chunk_components = class_chunk_components[mask]

        processed_chunks.append(class_chunk_components)

    # filter on added or changed
    class_components = pd.concat(processed_chunks)
    components_zero = class_components[class_components['changeHasOccurredMetric'] == '0']
    components_true = class_components[class_components['changeHasOccurredMetric'].isin(['true', 'True', True])]
    components = components_zero.append(components_true, ignore_index=True)
    store_dates_for_files(components[['version', 'name']])
    return components[['version', 'name']]
