import pandas as pd
from config import results_file


def get_analysis_results():
    dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%y')
    return pd.read_csv(results_file, parse_dates=['analysis_start_date', 'analysis_end_date'], date_parser=dateparse)
    # Parse dates


def label_points(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']), fontsize=4)

