from Utility import read_or_create_csv
from config import results_file
import pandas as pd


# project = project name and row index (e.g "cassandra")
# key = column name
# value = value to be placed at (project, key) in the results csv
def add_result(project, key, value):
    result_df = read_or_create_csv(results_file)
    if 'project' not in result_df:
        result_df = pd.DataFrame(columns=['project'])

    if result_df.isin({'project': project}):
        result_df.append({project: project})