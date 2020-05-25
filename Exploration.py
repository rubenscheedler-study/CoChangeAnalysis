import datetime

import pandas as pd
from matplotlib_venn import venn3, venn2

from FOAnalyzer import FOAnalyzer
from ClassFOAnalysis import ClassFOAnalysis
from PackageFOAnalysis import PackageFOAnalysis
from Utility import read_filename_pairs, get_project_class_smells_in_range, sort_tuple_elements, order_file1_and_file2, \
    find_pairs_with_date_range, find_pairs, to_unique_file_tuples, get_project_package_smells_in_range, order_package1_and_package2
from config import output_directory, input_directory
from matplotlib import pyplot as plt

analyzer = FOAnalyzer()
class_level_analyzer = ClassFOAnalysis()
package_level_analyzer = PackageFOAnalysis()
def run_exploration():
    calculate_smell_co_change_overlaps()


def calculate_smell_co_change_overlaps():
    dtw_pairs = set(overlap_dtw())
    mba_pairs = set(overlap_mba())
    fo_pairs = set(print_overlap_fo())
    venn3([dtw_pairs, mba_pairs, fo_pairs], ('dtw', 'mba', 'fo'))
    plt.show()


def overlap_dtw():
    return print_overlap_of_algorithm("DTW", output_directory + "/file_pairs_dtw.csv", output_directory + "/dtw.csv")


def print_overlap_of_algorithm(name, file_containing_all_pairs, file_containing_co_changes, include_class_level=True, include_package_level=True):
    print("--- Overlap ", name, " co-changes and smells: ---")

    all_pairs_df = order_package1_and_package2(order_file1_and_file2(find_pairs(file_containing_all_pairs)))
    cc_pairs_df = order_package1_and_package2(order_file1_and_file2(find_pairs_with_date_range(file_containing_co_changes, '%Y-%m-%d %H:%M:%S')))
    # Get raw smell pairs
    # package_smelling_co_changing_pairs, package_all_smelly_pairs, package_co_changed_pairs, package_all_pairs = package_level_analyzer.get_pairs()
    # class_smelling_co_changing_pairs, class_all_smelly_pairs, class_co_changed_pairs, class_all_pairs = class_level_analyzer.get_pairs()
    # smelly_pairs = package_all_smelly_pairs.union(class_all_smelly_pairs)  # filter duplicates
    # smelly_pairs_df = pd.Dataframe(smelly_pairs, columns=['file1', 'file2'])

    class_smell_pairs_with_date = order_file1_and_file2(get_project_class_smells_in_range())  # df: file1, file2
    class_smell_pairs_with_date = all_pairs_df.merge(class_smell_pairs_with_date, how='inner', left_on=['file1', 'file2'], right_on=['file1', 'file2'])

    package_smell_pairs_with_date = order_package1_and_package2(get_project_package_smells_in_range())  # df: package1, package2
    package_smell_pairs_with_date = all_pairs_df.merge(package_smell_pairs_with_date, how='inner', left_on=['package1', 'package2'], right_on=['package1', 'package2'])

    smell_pairs_with_date = class_smell_pairs_with_date.append(package_smell_pairs_with_date[["file1", "file2"]], sort=False)  # df: file1, file2
    distinct_smelly_pairs = to_unique_file_tuples(smell_pairs_with_date)  # (file1, file2)

    all_file_pair_tuples = set(all_pairs_df.apply(lambda row: (row.file1, row.file2), axis=1))

    relevant_smelly_pairs = set(distinct_smelly_pairs).intersection(all_file_pair_tuples)

    overlapping_pairs = to_unique_file_tuples(analyzer.perform_chunkified_pair_join(cc_pairs_df, smell_pairs_with_date))

    print(name, " all pairs:\t\t", len(all_pairs_df))
    print(name, " co-change pairs:\t\t", len(cc_pairs_df))
    print("All smell pairs:\t\t", len(distinct_smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(overlapping_pairs))
    print("Overlap ratio:\t\t", 0 if len(relevant_smelly_pairs) == 0 else 100 * (len(overlapping_pairs) / len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    for pair in overlapping_pairs:
        print(pair[0], ", ", pair[1])
    return overlapping_pairs

def overlap_mba():
    return print_overlap_of_algorithm("MBA", output_directory + "/file_pairs_mba.csv", output_directory + "/mba.csv")



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
