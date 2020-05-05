from matplotlib_venn import venn3, venn2

from FOAnalysis import get_pairs
from Utility import read_filename_pairs, get_project_smells_in_range, sort_tuple_elements
from config import output_directory, input_directory
from matplotlib import pyplot as plt

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

    dtw_all_pairs = sort_tuple_elements(read_filename_pairs(output_directory + "/file_pairs_dtw.csv"))
    dtw_cc_pairs = sort_tuple_elements(read_filename_pairs(output_directory + "/dtw.csv"))
    # Get raw smell pairs
    smell_pairs_with_date = get_project_smells_in_range(False)
    smelly_pairs = set(smell_pairs_with_date.apply(lambda row: (row.file1, row.file2), axis=1))

    distinct_smelly_pairs = set(sort_tuple_elements(smelly_pairs))
    relevant_smelly_pairs = set(distinct_smelly_pairs).intersection(dtw_all_pairs)

    overlapping_pairs = relevant_smelly_pairs.intersection(dtw_cc_pairs)

    print("DTW all pairs:\t\t", len(dtw_all_pairs))
    print("DTW co-change pairs:\t\t", len(dtw_cc_pairs))
    print("All smell pairs:\t\t", len(smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(overlapping_pairs))
    print("Overlap ratio:\t\t", 100*(len(overlapping_pairs)/len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    for pair in overlapping_pairs:
        print(pair[0], ", ", pair[1])
    return overlapping_pairs

def print_overlap_mba():
    print("--- Overlap MBA co-changes and smells: ---")
    mba_all_pairs = sort_tuple_elements(read_filename_pairs(output_directory + "/file_pairs_mba.csv"))
    mba_cc_pairs = sort_tuple_elements(read_filename_pairs(output_directory + "/mba.csv"))

    # Get raw smell pairs
    smell_pairs_with_date = get_project_smells_in_range(False)
    smelly_pairs = set(smell_pairs_with_date.apply(lambda row: (row.file1, row.file2), axis=1))

    distinct_smelly_pairs = set(sort_tuple_elements(smelly_pairs))
    relevant_smelly_pairs = set(distinct_smelly_pairs).intersection(mba_all_pairs)

    overlapping_pairs = relevant_smelly_pairs.intersection(mba_cc_pairs)

    print("MBA all pairs:\t\t", len(mba_all_pairs))
    print("MBA co-change pairs:\t\t", len(mba_cc_pairs))
    print("All smell pairs:\t\t", len(smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(overlapping_pairs))
    print("Overlap ratio:\t\t", 100*(len(overlapping_pairs)/len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    for pair in overlapping_pairs:
        print(pair[0], ", ", pair[1])
    return overlapping_pairs


def print_overlap_fo():
    print("--- Overlap Fuzzy Overlap co-changes and smells: ---")
    smelling_co_changing_pairs, smelly_pairs, fo_cc_pairs, fo_all_pairs = get_pairs()
    relevant_smelly_pairs = smelly_pairs.intersection(fo_all_pairs)

    print("FO all pairs:\t\t", len(fo_all_pairs))
    print("FO co-change pairs:\t\t", len(fo_cc_pairs))
    print("All smell pairs:\t\t", len(smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(smelling_co_changing_pairs))
    print("Overlap ratio:\t\t", 100 * (len(smelling_co_changing_pairs) / len(relevant_smelly_pairs)))
    print("overlapping pairs:")
    for pair in smelling_co_changing_pairs:
        print(pair[0], ", ", pair[1])
    return smelling_co_changing_pairs

