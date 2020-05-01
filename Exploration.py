from Utility import read_filename_pairs, get_project_smells_in_range, sort_tuple_elements
from config import output_directory, input_directory


def run_exploration():
    calculate_smell_co_change_overlaps()


def calculate_smell_co_change_overlaps():
    # Get raw smell pairs
    smell_pairs_with_date = get_project_smells_in_range()

    print_overlap_dtw(smell_pairs_with_date)
    print_overlap_mba(smell_pairs_with_date)
    print_overlap_fo(smell_pairs_with_date)


def print_overlap_dtw(smell_pairs_with_date):
    print("--- Overlap DTW co-changes and smells: ---")
    dtw_all_pairs = read_filename_pairs(output_directory + "/file_pairs_dtw.csv")
    dtw_cc_pairs = sort_tuple_elements(read_filename_pairs(output_directory + "/dtw.csv"))

    smelly_pairs = set(smell_pairs_with_date.apply(lambda row: (row.file1, row.file2), axis=1))
    distinct_smelly_pairs = set(sort_tuple_elements(smelly_pairs))
    relevant_smelly_pairs = set(distinct_smelly_pairs).intersection(dtw_all_pairs)

    overlapping_pairs = relevant_smelly_pairs.intersection(dtw_cc_pairs)

    print("DTW all pairs:\t\t", len(dtw_all_pairs))
    print("DTW co-change pairs:\t\t", len(dtw_cc_pairs))
    print("All smell pairs:\t\t", len(smelly_pairs))
    print("Relevant smell pairs:\t\t", len(relevant_smelly_pairs))
    print("Overlapping pairs:\t\t", len(overlapping_pairs))
    print("Overlap ratio:\t\t", 100*(len(overlapping_pairs)/len(dtw_all_pairs)))


def print_overlap_mba(smell_pairs_with_date):
    mba_all_pairs = read_filename_pairs(output_directory + "/file_pairs_mba.csv")
    mba_cc_pairs = read_filename_pairs(output_directory + "/mba.csv")


def print_overlap_fo(smell_pairs_with_date):
    fo_all_pairs = read_filename_pairs(input_directory + "/file_pairs.csv")
    fo_cc_pairs = read_filename_pairs(input_directory + "/cochanges.csv")


run_exploration()
