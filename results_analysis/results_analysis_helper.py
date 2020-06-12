import pandas as pd


def get_analysis_results():
    dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%y')
    return pd.read_csv('analysis_results_c.csv', parse_dates=['analysis_start_date', 'analysis_end_date'], date_parser=dateparse)
    # Parse dates


def label_points(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']), fontsize=4)

