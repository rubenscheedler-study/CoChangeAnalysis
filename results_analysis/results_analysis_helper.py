import pandas as pd


def get_analysis_results():
    dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%y')
    return pd.read_csv('analysis_results.csv', parse_dates=['analysis_start_date', 'analysis_end_date'], date_parser=dateparse)
    # Parse dates


def label_points(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']), fontsize=4)


def date_range_histogram(start_dates, end_dates, left_bound_date, right_bound_date, bins=100):
    # Create the bins
    return None

def date_range(start, end, bins):
    from datetime import datetime
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    diff = (end - start) / bins
    for i in range(bins):
        yield (start + diff * i).strftime("%Y%m%d")
    yield end.strftime("%Y%m%d")
