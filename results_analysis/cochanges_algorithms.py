import os
from collections import namedtuple
from datetime import timedelta, datetime
from matplotlib_venn import venn3

import matplotlib.pyplot as plt

import config
from helper_scripts.file_pair_helper import find_pairs_with_date_range, to_unique_file_tuples
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
    analysed_projects = [f.name for f in os.scandir('output') if f.is_dir()]
    for proj in analysed_projects:
        if proj != 'mybatis-3':
            continue

        data_row = analysis_results.loc[analysis_results['project'] == proj]
        start_date = data_row.analysis_start_date.iloc[0]
        end_date = data_row.analysis_end_date.iloc[0]
        cochanges_fo = find_pairs_with_date_range('input/' + proj + '/cochanges.csv', '%d-%m-%Y')
        cochanges_dtw = find_pairs_with_date_range('output/' + proj + '/dtw.csv', '%Y-%m-%d %H:%M:%S')
        cochanges_mba = find_pairs_with_date_range('output/' + proj + '/mba.csv', '%Y-%m-%d %H:%M:%S')
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
        plt.title(proj)
        plt.show()


def algorithms_venn():
    analysed_projects = [f.name for f in os.scandir('output') if f.is_dir()]
    for proj in analysed_projects:
        if proj != 'swagger-core':
            continue
        cochanges_fo = to_unique_file_tuples(
            find_pairs_with_date_range('input/' + proj + '/cochanges.csv', '%d-%m-%Y'))
        cochanges_dtw = to_unique_file_tuples(
            find_pairs_with_date_range('output/' + proj + '/dtw.csv', '%Y-%m-%d %H:%M:%S'))
        cochanges_mba = to_unique_file_tuples(
            find_pairs_with_date_range('output/' + proj + '/mba.csv', '%Y-%m-%d %H:%M:%S'))
        venn3([cochanges_dtw, cochanges_mba, cochanges_fo], ('dtw', 'mba', 'fo'))
        plt.title(proj)
        plt.show()
