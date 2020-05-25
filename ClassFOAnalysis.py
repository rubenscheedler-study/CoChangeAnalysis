
import pandas as pd

from FOAnalyzer import FOAnalyzer
from Utility import get_project_class_smells_in_range, order_file1_and_file2, \
    get_class_from_package, to_unique_file_tuples, \
    find_pairs_with_date_range
from config import input_directory, output_directory


class ClassFOAnalysis:

    def __init__(self):
        self.analyzer = FOAnalyzer()

    # Executes a range of relevant tests on class-level co-changes and smells.
    def execute(self):
        smelling_co_changing_pairs, all_smelly_pairs, co_changed_pairs, all_pairs = self.get_pairs()
        print("class analysis results:")
        self.analyzer.analyze_results(smelling_co_changing_pairs, all_smelly_pairs, co_changed_pairs, all_pairs)

    # Calculates the contingency table values for class level file pairs
    def get_pairs(self):
        # All pairs formed from all files changed in the relevant time frame.
        all_pairs_df = pd.read_csv(input_directory + "/file_pairs.csv")
        #all_pairs_df['file1'] = [get_class_from_package(s, True) for s in all_pairs_df["file1"].values]
        #all_pairs_df['file2'] = [get_class_from_package(s, True) for s in all_pairs_df["file2"].values]
        all_pairs_df = order_file1_and_file2(all_pairs_df)

        # All co-changed pairs with corresponding date range.
        co_changed_pairs_with_date_range = order_file1_and_file2(find_pairs_with_date_range(input_directory + "/cochanges.csv", '%d-%m-%Y'))
        co_changed_pairs = to_unique_file_tuples(co_changed_pairs_with_date_range)

        # All smelly pairs of the whole analyzed history of the project.
        smelly_pairs_with_date_df = order_file1_and_file2(get_project_class_smells_in_range())
        #smelly_pairs_with_date_df.to_csv(output_directory + '/test.csv')
        # Find intersection between smells and co-changes.
        smelling_co_changing_pairs_df = self.analyzer.perform_chunkified_pair_join(co_changed_pairs_with_date_range, smelly_pairs_with_date_df)
        smelling_co_changing_pairs = to_unique_file_tuples(smelling_co_changing_pairs_df)

        all_smelly_pairs = to_unique_file_tuples(smelly_pairs_with_date_df)
        all_pairs = to_unique_file_tuples(all_pairs_df)

        return smelling_co_changing_pairs, all_smelly_pairs, co_changed_pairs, all_pairs
