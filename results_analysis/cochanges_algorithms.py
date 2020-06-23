import os
from collections import namedtuple
from datetime import timedelta, datetime
from matplotlib_venn import venn3, venn2

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

def export_legend():
    labels = ['FO', 'DTW', 'MBA']

    fig = plt.figure()
    fig_legend = plt.figure(figsize=(2, 1.25))
    ax = fig.add_subplot(111)
    lines = ax.plot(range(2), range(2), range(2), range(2), range(2), range(2), range(2), range(2))
    fig_legend.legend(lines, labels, loc='center', frameon=False)
    plt.savefig('Images/legend.png', bbox_inches='tight')
    plt.show()

def cochanges_over_time():
    analysis_results = get_analysis_results()
    analysed_projects = [f.name for f in os.scandir('output') if f.is_dir()]
    export_legend()
    for proj in analysed_projects:
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
        plt.rcParams.update({'font.size': 15})
        plt.plot(x, fo, label='fo')
        plt.plot(x, dtw, label='dtw')
        plt.plot(x, mba, label='mba')
        plt.title(proj)
        plt.xticks(rotation=45)
        plt.savefig('Images/cc_over_time_'+proj+'.png', bbox_inches='tight')
        plt.show()


def algorithms_venn():
    analysed_projects = [f.name for f in os.scandir('output') if f.is_dir()]
    for proj in analysed_projects:
        cochanges_fo = to_unique_file_tuples(
            find_pairs_with_date_range('input/' + proj + '/cochanges.csv', '%d-%m-%Y'))
        cochanges_dtw = to_unique_file_tuples(
            find_pairs_with_date_range('output/' + proj + '/dtw.csv', '%Y-%m-%d %H:%M:%S'))
        cochanges_mba = to_unique_file_tuples(
            find_pairs_with_date_range('output/' + proj + '/mba.csv', '%Y-%m-%d %H:%M:%S'))

        plt.rcParams.update({'font.size': 15})
        if len(cochanges_mba) == 0:
            venn2([cochanges_dtw, cochanges_fo], ('dtw', 'fo'))
        else:
            venn3([cochanges_dtw, cochanges_mba, cochanges_fo], ('dtw', 'mba', 'fo'))
        plt.title(proj)
        plt.savefig('Images/venn_'+proj+'.png', bbox_inches='tight')
        plt.show()
        print(proj)
        print('overlap wrt fo: ', len(cochanges_fo.intersection(cochanges_dtw)) / len(cochanges_fo) * 100)
        print('overlap wrt dtw: ', len(cochanges_fo.intersection(cochanges_dtw)) / len(cochanges_dtw) * 100)
        print('overlap wrt union: ', len(cochanges_fo.intersection(cochanges_dtw)) / len(cochanges_dtw.union(cochanges_fo)) * 100)


def cochange_percentages():
    analysed_projects = [f.name for f in os.scandir('output') if f.is_dir()]
    for proj in analysed_projects:
        cochanges_fo = to_unique_file_tuples(
            find_pairs_with_date_range('input/' + proj + '/cochanges.csv', '%d-%m-%Y'))
        cochanges_dtw = to_unique_file_tuples(
            find_pairs_with_date_range('output/' + proj + '/dtw.csv', '%Y-%m-%d %H:%M:%S'))
        cochanges_mba = to_unique_file_tuples(
            find_pairs_with_date_range('output/' + proj + '/mba.csv', '%Y-%m-%d %H:%M:%S'))
        all_pairs = pd.read_csv('input/' + proj + '/file_pairs.csv')[['file1', 'file2']]
        all_pairs.drop_duplicates(inplace=True)
        print(proj)
        print('fo: ', len(cochanges_fo))
        print('dtw: ', len(cochanges_dtw))
        print('mba: ', len(cochanges_mba))
        print('total: ', len(all_pairs))
        print('fo percentage: ', len(cochanges_fo) / len(all_pairs) * 100)
        print('dtw percentage: ', len(cochanges_dtw) / len(all_pairs) * 100)
        print('mba percentage: ', len(cochanges_mba) / len(all_pairs) * 100)
