import os

import numpy as np

from config import results_file
import pandas as pd


# project = project name and row index (e.g "cassandra")
# key = column name
# value = value to be placed at (project, key) in the results csv
def add_result(project, key, value):

    # Check if we already have a results file
    if os.path.isfile(results_file):
        result_df = pd.read_csv(results_file, index_col=False)
    else:
        # Create df with project column
        result_df = pd.DataFrame(columns=['project'])

    # Create row for project
    if len(result_df[result_df.project == project]) == 0:
        result_df = result_df.append(pd.DataFrame([project], columns=['project']), ignore_index=True)
    # Create column `key`
    if key not in result_df:
        result_df.loc[:, key] = np.nan
    # Get row of the project and assign the value
    result_df.loc[(result_df.project == project), [key]] = value
    # Update the csv
    result_df.to_csv(results_file, index=False)
