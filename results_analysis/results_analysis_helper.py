import pandas as pd


def get_analysis_results():
    dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%y')
    return pd.read_csv('analysis_results.csv', parse_dates=['analysis_start_date', 'analysis_end_date'], date_parser=dateparse)
    # Parse dates


