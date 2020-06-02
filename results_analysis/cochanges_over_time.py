from collections import namedtuple
from datetime import timedelta, datetime

import matplotlib.pyplot as plt

import config
from helper_scripts.file_pair_helper import find_pairs_with_date_range
from results_analysis.results_analysis_helper import get_analysis_results

def daterange_in_weeks(date1, date2):
    date_list = []
    current_date = date1
    date_list.append(current_date)
    while (current_date + timedelta(weeks=1)) < date2:
        current_date = current_date + timedelta(weeks=1)
        date_list.append(current_date)
    return date_list


def cochanges_over_time():
    analysis_results = get_analysis_results()
    data_row = analysis_results.loc[analysis_results['project'] == config.project_name]
    start_date = data_row.analysis_start_date.iloc[0]
    end_date = data_row.analysis_end_date.iloc[0]
    cochanges_fo = find_pairs_with_date_range(config.input_directory + '/cochanges.csv', '%d-%m-%Y')
    cochanges_dtw = find_pairs_with_date_range(config.output_directory + '/dtw.csv', '%Y-%m-%d %H:%M:%S')
    cochanges_mba = find_pairs_with_date_range(config.output_directory + '/mba.csv', '%Y-%m-%d %H:%M:%S')
    results = {}
    ResultRow = namedtuple('ResultRow', ['fo', 'dtw', 'mba'])
    for date in daterange_in_weeks(start_date, end_date):
        fo = cochanges_fo[cochanges_fo['parsedStartDate'] <= date]
        fo = fo[date <= fo['parsedEndDate']]
        dtw = cochanges_dtw[cochanges_dtw['parsedStartDate'] <= date]
        dtw = dtw[date <= dtw['parsedEndDate']]
        mba = cochanges_mba[cochanges_mba['parsedStartDate'] <= date]
        mba = mba[date <= mba['parsedEndDate']]
        results[date] = ResultRow(fo=fo.shape[0], dtw=dtw.shape[0], mba=mba.shape[0])

    result_list = sorted(results.items())
    x, y = zip(*result_list)
    fo = [fo for fo, dtw, mba in y]
    dtw = [dtw for fo, dtw, mba in y]
    mba = [mba for fo, dtw, mba in y]
    x = [d.date() for d in x]
    plt.plot(x, fo, label='fo')
    plt.plot(x, dtw, label='dtw')
    plt.plot(x, mba, label='mba')
    plt.legend(loc="upper left")
    plt.show()