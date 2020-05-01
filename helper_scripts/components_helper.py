import pandas as pd
from config import input_directory


def get_components():
    components = pd.read_csv(input_directory + "/component-characteristics-consecOnly.csv")
    # only consider classes, not packages
    class_components = components[components['type'] == 'class']
    # filter on added or changed
    components_zero = class_components[class_components['changeHasOccurredMetric'] == '0']
    components_true = class_components[class_components['changeHasOccurredMetric'] == True]
    components = components_zero.append(components_true, ignore_index=True)
    return components[['version', 'name']]