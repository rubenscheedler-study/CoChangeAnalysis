import datetime

import pandas as pd
from matplotlib_venn import venn3, venn2

from FOAnalyzer import FOAnalyzer
from ClassFOAnalysis import ClassFOAnalysis
from PackageFOAnalysis import PackageFOAnalysis
from Utility import read_filename_pairs, get_project_class_smells_in_range, sort_tuple_elements, order_file1_and_file2, \
    find_pairs_with_date_range, find_pairs, to_unique_file_tuples
from config import output_directory, input_directory
from matplotlib import pyplot as plt

analyzer = FOAnalyzer()
class_level_analyzer = ClassFOAnalysis()
package_level_analyzer = PackageFOAnalysis()
def run_exploration():
    calculate_smell_co_change_overlaps()


def calculate_smell_co_change_overlaps():
    dtw_pairs = set(print_overlap_dtw())
    mba_pairs = set(print_overlap_mba())
    fo_pairs = set(print_overlap_fo())
    venn3([dtw_pairs, mba_pairs, fo_pairs], ('dtw', 'mba', 'fo'))
    plt.show()


def print_overlap_dtw():
    print("--- Overlap DTW co-changes and smells: ---")

    dtw_all_pairs = order_file1_and_file2(find_pairs(output_directory + "/file_pairs_dtw.csv"))
    dtw_cc_pairs = order_file1_and_file2(find_pairs_with_date_range(output_directory + "/dtw.csv", '%Y-%m-%d %H:%M:%S'))
    # Get raw smell pairs
    package_smelling_co_changing_pairs, package_all_smelly_pairs, package_co_changed_pairs, package_all_pairs = package_level_analyzer.get_pairs()
    class_smelling_co_changing_pairs, class_all_smelly_pairs, class_co_changed_pairs, class_all_pairs = class_level_analyzer.get_pairs()
    smelly_pairs = package_all_smelly_pairs.union(class_all_smelly_pairs)  # filter duplicates
    smelly_pairs_df = pd.Dataframe(smelly_pairs, columns=['file1', 'file2'])

    #smell_pairs_with_date = order_file1_and_file2(get_project_class_smells_in_range(True))
    dtw_as_tuple = set(dtw_all_pairs.apply(lambda row: (row.file1, row.file2), axis=1))

    distinct_smelly_pairs = set(sort_tuple_elements(smelly_pairs))
    relevant_smelly_pairs = set(distinct_smelly_pairs).intersection(dtw_as_tuple)

    overlapping_pairs = to_unique_file_tuples(analyzer.get_co_changed_smelly_pairs(dtw_cc_pairs, smelly_pairs_df))

    print("DTW all pairs:\t\t", len(dtw_all_pairs))
    print("DTW co-change pairs:\t\t", len(dtw_cc_pairs))
    print("All smell pairs:\t\t", len(smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(overlapping_pairs))
    print("Overlap ratio:\t\t", 0 if len(relevant_smelly_pairs) == 0 else 100 * (len(overlapping_pairs) / len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    for pair in overlapping_pairs:
        print(pair[0], ", ", pair[1])
    return overlapping_pairs


def print_overlap_mba():
    print("--- Overlap MBA co-changes and smells: ---")
    mba_all_pairs = order_file1_and_file2(find_pairs(output_directory + "/file_pairs_mba.csv"))
    mba_cc_pairs = order_file1_and_file2(find_pairs_with_date_range(output_directory + "/mba.csv", '%Y-%m-%d %H:%M:%S'))

    # Get raw smell pairs
    smell_pairs_with_date = order_file1_and_file2(get_project_class_smells_in_range(True))
    smelly_pairs = set(smell_pairs_with_date.apply(lambda row: (row.file1, row.file2), axis=1))
    mba_as_tuple = set(mba_all_pairs.apply(lambda row: (row.file1, row.file2), axis=1))

    distinct_smelly_pairs = set(sort_tuple_elements(smelly_pairs))
    relevant_smelly_pairs = set(distinct_smelly_pairs).intersection(mba_as_tuple)

    overlapping_pairs = to_unique_file_tuples(analyzer.get_co_changed_smelly_pairs(mba_cc_pairs, smell_pairs_with_date))

    print("MBA all pairs:\t\t", len(mba_all_pairs))
    print("MBA co-change pairs:\t\t", len(mba_cc_pairs))
    print("All smell pairs:\t\t", len(smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(overlapping_pairs))
    print("Overlap ratio:\t\t", 0 if len(relevant_smelly_pairs) == 0 else 100 * (len(overlapping_pairs) / len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    for pair in overlapping_pairs:
        print(pair[0], ", ", pair[1])
    return overlapping_pairs


def print_overlap_fo():
    class_level_analyzer = ClassFOAnalysis()
    print("--- Overlap Fuzzy Overlap co-changes and smells: ---")
    smelling_co_changing_pairs, smelly_pairs, fo_cc_pairs, fo_all_pairs = class_level_analyzer.get_pairs()
    relevant_smelly_pairs = smelly_pairs.intersection(fo_all_pairs)

    print("FO all pairs:\t\t", len(fo_all_pairs))
    print("FO co-change pairs:\t\t", len(fo_cc_pairs))
    print("All smell pairs:\t\t", len(smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(smelling_co_changing_pairs))
    print("Overlap ratio:\t\t", 0 if len(relevant_smelly_pairs) == 0 else 100 * (len(smelling_co_changing_pairs) / len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    for pair in smelling_co_changing_pairs:
        print(pair[0], ", ", pair[1])
    return smelling_co_changing_pairs
