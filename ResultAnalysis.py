import datetime
import itertools
from functools import reduce

import numpy as np
import pandas as pd
from itertools import combinations, chain
from scipy import stats
from scipy.stats import chi2

from Utility import read_filename_pairs, sort_tuple_elements, get_project_smells_in_range
from config import analysis_start_date, analysis_end_date, input_directory


def analyze_results():

    # All pairs formed from all files changed in the relevant time frame.
    all_pairs = sort_tuple_elements(read_filename_pairs(input_directory + "/file_pairs.csv"))
    # All co-changed pairs with corresponding date range.
    co_changed_pairs_with_date_range = find_co_changed_pairs_with_date_range()

    co_changed_pairs_with_date_range['parsedStartDate'] = co_changed_pairs_with_date_range['startdate'].map(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
    co_changed_pairs_with_date_range['parsedEndDate'] = co_changed_pairs_with_date_range['enddate'].map(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
    # All smelly pairs of the whole analyzed history of the project.
    smelly_pairs_with_date = get_project_smells_in_range()

    distinct_smelly_pairs = set(smelly_pairs_with_date.apply(lambda row: (row.file1, row.file2), axis=1))
    smelly_pairs = sort_tuple_elements(distinct_smelly_pairs)
    # Only keep the smelly pairs that are part of 'all_pairs'
    relevant_smelly_pairs = set(smelly_pairs).intersection(all_pairs)
    co_changed_pairs = sort_tuple_elements(list(zip(co_changed_pairs_with_date_range.file1, co_changed_pairs_with_date_range.file2)))

    # Calculate sets for contingency table
    non_smelling_non_co_changing_pairs = set(all_pairs).difference(relevant_smelly_pairs).difference(co_changed_pairs)
    non_smelling_co_changing_pairs = set(co_changed_pairs).difference(relevant_smelly_pairs)
    smelling_non_co_changing_pairs = set(relevant_smelly_pairs).difference(co_changed_pairs)
    smelling_co_changing_pairs = get_co_changed_smelly_pairs(co_changed_pairs_with_date_range, smelly_pairs_with_date)

    # Save the pairs in csv files
    pd.DataFrame(list(non_smelling_non_co_changing_pairs)).to_csv('output/non_smelling_non_co_changing_pairs.csv', index=False, header=True)
    pd.DataFrame(list(non_smelling_co_changing_pairs)).to_csv('output/non_smelling_co_changing_pairs.csv', index=False, header=True)
    pd.DataFrame(list(smelling_non_co_changing_pairs)).to_csv('output/smelling_non_co_changing_pairs.csv', index=False, header=True)
    pd.DataFrame(list(smelling_co_changing_pairs)).to_csv('output/smelling_co_changing_pairs.csv', index=False, header=True)

    # Calculate values of the contingency table cells
    non_smelling_non_co_changing_pairs_size = len(non_smelling_non_co_changing_pairs)
    non_smelling_co_changing_pairs_size = len(non_smelling_co_changing_pairs)
    smelling_non_co_changing_pairs_size = len(smelling_non_co_changing_pairs)
    smelling_co_changing_pairs_size = len(smelling_co_changing_pairs)

    # total amount of observations
    n = non_smelling_non_co_changing_pairs_size + non_smelling_co_changing_pairs_size + smelling_non_co_changing_pairs_size + smelling_co_changing_pairs_size
    print("general information:")
    print("all_pairs size: " + str(len(all_pairs)))
    print("smelly_pairs size: " + str(len(smelly_pairs)))
    print("relevant_smelly_pairs size: " + str(len(relevant_smelly_pairs)))
    print("co_changed_pairs size: " + str(len(co_changed_pairs)))
    print("\n")

    perform_chi2_analysis(non_smelling_non_co_changing_pairs_size, non_smelling_co_changing_pairs_size, smelling_non_co_changing_pairs_size, smelling_co_changing_pairs_size, n)
    perform_fisher(non_smelling_non_co_changing_pairs_size, non_smelling_co_changing_pairs_size, smelling_non_co_changing_pairs_size, smelling_co_changing_pairs_size)


def perform_fisher(non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs):
    oddsratio, pvalue = stats.fisher_exact([[non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs], [smelling_non_co_changing_pairs, smelling_co_changing_pairs]])
    print("Fisher values:")
    print("oddsratio: " + str(oddsratio))
    print("p-value: " + str(pvalue))
    print("\n")


def perform_chi2_analysis(non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs, n):
    print("chi2 values:")
    print("non_smelling_non_co_changing_pairs: " + str(non_smelling_non_co_changing_pairs))
    print("non_smelling_co_changing_pairs: " + str(non_smelling_co_changing_pairs))
    print("smelling_non_co_changing_pairs: " + str(smelling_non_co_changing_pairs))
    print("smelling_co_changing_pairs: " + str(smelling_co_changing_pairs))

    # Calculate chi2
    chi2_stat, p_val, dof, ex = stats.chi2_contingency([[non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs], [smelling_non_co_changing_pairs, smelling_co_changing_pairs]])
    # calculate critical value
    significance = 0.05
    p = 1 - significance
    critical_value = chi2.ppf(p, dof)
    # calculate phi value
    phi = np.sqrt(chi2_stat / n)
    print("===Chi2 Stat vs critical value===")
    print('chi=%.6f, critical value=%.6f\n' % (chi2_stat, critical_value))
    print('oddsratio: %.6f' % odds_ratio(non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs))
    print("\n")
    print("===Phi value[0.1: small | 0.3: average | 0.5: large]===")
    print(phi)
    print("\n")
    print("===Degrees of Freedom===")
    print(dof)
    print("\n")
    print("===P-Value===")
    print(p_val)
    print("\n")
    print("===Contingency Table===")
    print(ex)


def odds_ratio(non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs):
    return (non_smelling_non_co_changing_pairs*smelling_co_changing_pairs)/(non_smelling_co_changing_pairs*smelling_non_co_changing_pairs)


def find_co_changed_pairs_with_date_range():
    return pd.read_csv(input_directory + "/cochanges.csv")


# Returns all co-changes that have a matching smell.
def get_co_changed_smelly_pairs(co_change_df, smell_df):
    co_changes_smells = co_change_df.merge(smell_df, how='inner', left_on=['file1', 'file2'], right_on=['file1', 'file2'])
    matching_co_changes = co_changes_smells[co_changes_smells.apply(lambda row: row['parsedStartDate'] <= row['parsedVersionDate'] <= row['parsedEndDate'], axis=1)]
    return set(list(zip(matching_co_changes.file1, matching_co_changes.file2)))





analyze_results()
