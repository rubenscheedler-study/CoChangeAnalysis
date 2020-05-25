import numpy as np
import pandas as pd
from itertools import combinations, chain
from scipy import stats
from scipy.stats import chi2

from FOAnalyzer import FOAnalyzer
from Utility import order_package1_and_package2, find_pairs_with_date_range, to_distinct_package_tuples, get_project_package_smells_in_range, order_file1_and_file2, to_unique_file_tuples
from config import input_directory


class PackageFOAnalysis:

    def __init__(self):
        self.analyzer = FOAnalyzer()

    # Executes a range of relevant tests on class-level co-changes and smells.
    def execute(self):
        smelling_co_changing_pairs, all_smelly_pairs, co_changed_pairs, all_pairs = self.get_pairs()
        print("package analysis results:")
        self.analyzer.analyze_results(smelling_co_changing_pairs, all_smelly_pairs, co_changed_pairs, all_pairs)

    # Calculates the contingency table values for package level pairs
    def get_pairs(self):
        # All pairs formed from all files changed in the relevant time frame.
        all_pairs_df = pd.read_csv(input_directory + "/file_pairs.csv")
        all_pairs_df.dropna(inplace=True)
        all_pairs_df = order_package1_and_package2(order_file1_and_file2(all_pairs_df))

        # All co-changed pairs with corresponding date range.
        co_changes_df = find_pairs_with_date_range(input_directory + "/cochanges.csv", '%d-%m-%Y')
        co_changes_df.dropna(inplace=True)
        co_changed_pairs_with_date_range = order_package1_and_package2(order_file1_and_file2(co_changes_df))
        co_changed_pairs = list(zip(co_changed_pairs_with_date_range.file1, co_changed_pairs_with_date_range.file2))

        # All smelly pairs of the whole analyzed history of the project.
        smelly_pairs_with_date_df = order_package1_and_package2(get_project_package_smells_in_range())
        # Find what changed file pairs are part of a smelly package
        smelly_file_pairs = all_pairs_df.merge(smelly_pairs_with_date_df, how='inner', left_on=['package1', 'package2'], right_on=['package1', 'package2'])
        unique_smelly_file_pairs = to_unique_file_tuples(smelly_file_pairs)

        # Find intersection between smells and co-changes.
        smelling_co_changing_pairs_df = self.analyzer.get_co_changed_smelly_pairs(co_changed_pairs_with_date_range, smelly_file_pairs, level='file')
        smelling_co_changing_pairs = to_unique_file_tuples(smelling_co_changing_pairs_df)

        all_pairs = list(zip(all_pairs_df.file1, all_pairs_df.file2))  # Here we keep track of allowed combinations. No need for duplicates.

        return smelling_co_changing_pairs, unique_smelly_file_pairs, co_changed_pairs, all_pairs
