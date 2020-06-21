import datetime
import gc

import pandas as pd
from matplotlib_venn import venn3, venn2

from Analyzer import Analyzer
from helper_scripts.file_pair_helper import order_file1_and_file2, order_package1_and_package2, to_unique_file_tuples, \
    find_pairs_with_date_range
from config import output_directory, input_directory, project_name, analysis_start_date
from matplotlib import pyplot as plt

from helper_scripts.join_helper import JoinHelper
from helper_scripts.pickle_helper import load_pickle, save_pickle
from helper_scripts.results_helper import add_result
from helper_scripts.smell_helper import get_project_class_smells_in_range, get_project_package_smells_in_range

analyzer = Analyzer()
join_helper = JoinHelper()
def run_exploration():
    calculate_smell_co_change_overlaps()


def calculate_smell_co_change_overlaps():
    overlap_dtw()
    overlap_mba()
    overlap_fo()


def print_overlap_of_algorithm(name, all_pairs_unsorted, co_changes_unsorted, include_class_level=True, include_package_level=True, calculate_chi_square=True, calculate_precede_values=True):
    print("--- Overlap ", name, " co-changes and smells: ---")
    all_pairs_unsorted = all_pairs_unsorted.drop(['file1Size', 'file2Size'], axis=1, errors='ignore')
    co_changes_unsorted = co_changes_unsorted.drop(['startdate', 'enddate', 'Unnamed: 0'], axis=1, errors='ignore')

    # Class level data
    all_pairs_no_package = all_pairs_unsorted.drop(['package1', 'package2'], axis=1)  # This drops rows without both packages. May only be done for class-level analysis
    all_pairs_no_package = order_file1_and_file2(all_pairs_no_package)
    cc_pairs_no_package = co_changes_unsorted.drop(['package1', 'package2'], axis=1)  # This drops rows without both packages. May only be done for class-level analysis
    cc_pairs_no_package = order_file1_and_file2(cc_pairs_no_package)

    class_smell_pairs_with_date = pd.DataFrame(columns=['file1', 'file2'])
    if include_class_level:
        class_smell_pairs_with_date = load_pickle("class_smell_pairs_with_date")
        if class_smell_pairs_with_date is None:
            class_smell_pairs_with_date = order_file1_and_file2(get_project_class_smells_in_range(calculate_precede_values))  # df: file1, file2
            # Find file pairs that are part of the same class-level smell:
            class_smell_pairs_with_date = join_helper.perform_chunkified_pair_join(all_pairs_no_package, class_smell_pairs_with_date, level='file', compare_dates=False)
            save_pickle(class_smell_pairs_with_date, "class_smell_pairs_with_date")


    # Package level data
    all_pairs_unsorted.dropna(inplace=True)
    co_changes_unsorted.dropna(inplace=True)
    all_pairs_with_package = order_package1_and_package2(order_file1_and_file2(all_pairs_unsorted))
    cc_pairs_with_package = order_package1_and_package2(order_file1_and_file2(co_changes_unsorted))

    package_smell_pairs_with_date = pd.DataFrame(columns=['file1', 'file2'])
    if include_package_level:
        package_smell_pairs_with_date = load_pickle("package_smell_pairs_with_date")
        if package_smell_pairs_with_date is None:
            package_smell_pairs_with_date = order_package1_and_package2(get_project_package_smells_in_range(calculate_precede_values))  # df: package1, package2
            # We want to find file pairs whose package are part of the same smell:
            package_smell_pairs_with_date = join_helper.perform_chunkified_pair_join(all_pairs_with_package, package_smell_pairs_with_date, level='package', compare_dates=False)
            # Note: we are interested in (file1, file2) in package_smell_pairs

            save_pickle(package_smell_pairs_with_date, "package_smell_pairs_with_date")

    # Combine the pairs
    df_list = [class_smell_pairs_with_date, package_smell_pairs_with_date]
    smell_pairs_with_date = pd.concat(df_list)

    del class_smell_pairs_with_date
    del package_smell_pairs_with_date
    gc.collect()

    distinct_smelly_pairs = to_unique_file_tuples(smell_pairs_with_date)  # (file1, file2)

    if include_class_level:
        all_file_pair_tuples = set(all_pairs_no_package.apply(lambda row: (row.file1, row.file2), axis=1))  # Use _no_package since we need the extra rows it contains
        cc_tuples = to_unique_file_tuples(cc_pairs_no_package)
        # Overlapping pairs contains at least: file1, file2, parsedSmellFirstDate, parsedSmellLastDate, parsedStartDate, parsedEndDate
        overlapping_cc_smells = join_helper.perform_chunkified_pair_join(cc_pairs_no_package, smell_pairs_with_date)
    else:
        all_file_pair_tuples = set(all_pairs_with_package.apply(lambda row: (row.file1, row.file2), axis=1))  # Only consider files we know the package of.
        cc_tuples = to_unique_file_tuples(cc_pairs_with_package)
        # Overlapping pairs contains at least: file1, file2, parsedSmellFirstDate, parsedSmellLastDate, parsedStartDate, parsedEndDate
        overlapping_cc_smells = join_helper.perform_chunkified_pair_join(cc_pairs_with_package, smell_pairs_with_date)

    relevant_smelly_pairs = set(distinct_smelly_pairs).intersection(all_file_pair_tuples)

    overlapping_pairs = to_unique_file_tuples(overlapping_cc_smells)

    # RQ4: Are smells introduced before or after files start co-changing?
    if calculate_precede_values and len(overlapping_cc_smells) > 0:
        # Filter smells and co-changes which are already present at the start of the analysis. We are not sure what their real start date is.
        print("unfiltered:", len(overlapping_cc_smells))
        overlapping_cc_smells = overlapping_cc_smells[overlapping_cc_smells['parsedSmellFirstDate'].dt.floor('d') != analysis_start_date.date()]
        print("after filtering smells: ", len(overlapping_cc_smells))  # Note: this counts joined rows
        overlapping_cc_smells = overlapping_cc_smells[overlapping_cc_smells['parsedStartDate'].dt.floor('d') != analysis_start_date.date()]
        print("filtered ccs: ", len(overlapping_cc_smells))

        # Compare the two start dates and count which is earlier how often. Also count ties!
        earlier_smell_rows = overlapping_cc_smells[overlapping_cc_smells['parsedSmellFirstDate'].dt.floor('d') < overlapping_cc_smells['parsedStartDate'].dt.floor('d')]
        earlier_ccs_rows = overlapping_cc_smells[overlapping_cc_smells['parsedStartDate'].dt.floor('d') < overlapping_cc_smells['parsedSmellFirstDate'].dt.floor('d')]
        tied_rows = overlapping_cc_smells[overlapping_cc_smells['parsedStartDate'].dt.floor('d') == overlapping_cc_smells['parsedSmellFirstDate'].dt.floor('d')]

        # group by: file1, file2, smellId
        earlier_smell_pairs = len(pd.unique(earlier_smell_rows[['file1', 'file2', 'uniqueSmellID']].values.ravel('K')))
        earlier_ccs_pairs = len(pd.unique(earlier_ccs_rows[['file1', 'file2', 'uniqueSmellID']].values.ravel('K')))
        tied_pairs = len(pd.unique(tied_rows[['file1', 'file2', 'uniqueSmellID']].values.ravel('K')))

        add_result(project_name, name + "_earlier_smell_pairs", earlier_smell_pairs)
        add_result(project_name, name + "_earlier_ccs_pairs", earlier_ccs_pairs)
        add_result(project_name, name + "_tied_pairs", tied_pairs)
    elif calculate_precede_values and len(overlapping_cc_smells) == 0:
        add_result(project_name, name + "_earlier_smell_pairs", 0)
        add_result(project_name, name + "_earlier_ccs_pairs", 0)
        add_result(project_name, name + "_tied_pairs", 0)

    # Store the balance in results
    print(name, " all pairs:\t\t", len(all_file_pair_tuples))
    print(name, " co-change pairs:\t\t", len(cc_tuples))
    print("All smell pairs:\t\t", len(distinct_smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(overlapping_pairs))
    print("Overlap ratio:\t\t", 0 if len(relevant_smelly_pairs) == 0 else 100 * (len(overlapping_pairs) / len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    add_result(project_name, name+"_all_pairs", len(all_file_pair_tuples))
    add_result(project_name, name + "_cc_pairs", len(cc_tuples))
    add_result(project_name, name + "_distinct_smelly_pairs", len(distinct_smelly_pairs))
    add_result(project_name, name + "_relevant_smelly_pairs", len(relevant_smelly_pairs))
    add_result(project_name, name + "_overlapping_pairs", len(overlapping_pairs))

    if calculate_chi_square:
        analyzer.analyze_results(name, overlapping_pairs, distinct_smelly_pairs, cc_tuples, all_file_pair_tuples)

    return overlapping_pairs


def overlap_dtw():
    return print_overlap_of_algorithm("DTW",
                                      pd.read_csv(input_directory + "/file_pairs.csv"),
                                      find_pairs_with_date_range(output_directory + "/dtw.csv", '%Y-%m-%d %H:%M:%S'),
                                      True,
                                      True,
                                      True,
                                      True)


def overlap_mba():
    return print_overlap_of_algorithm("MBA",
                                      pd.read_csv(input_directory + "/file_pairs.csv"),
                                      find_pairs_with_date_range(output_directory + "/mba.csv", '%Y-%m-%d %H:%M:%S'),
                                      True,
                                      True,
                                      True,
                                      True)


def overlap_fo():
    return print_overlap_of_algorithm("FO",
                                      pd.read_csv(input_directory + "/file_pairs.csv"),
                                      find_pairs_with_date_range(input_directory + "/cochanges.csv", '%d-%m-%Y'),
                                      True,
                                      True,
                                      True,
                                      True)

#
# Time of smell vs time of co-change
#
