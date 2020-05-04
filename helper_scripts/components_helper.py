import pandas as pd
from config import input_directory
from helper_scripts import Commit_date_helper
from helper_scripts.Commit_date_helper import store_dates_for_files


def get_components():
    components = pd.read_csv(input_directory + "/component-characteristics-consecOnly.csv")
    # only consider classes, not packages
    class_components = components[components['type'] == 'class']
    # filter on added or changed
    components_zero = class_components[class_components['changeHasOccurredMetric'] == '0']
    components_true = class_components[class_components['changeHasOccurredMetric'] == True]
    components = components_zero.append(components_true, ignore_index=True)
    store_dates_for_files(components[['version', 'name']])
    return components[['version', 'name']]
