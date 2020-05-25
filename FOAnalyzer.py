import numpy as np
from scipy import stats
from scipy.stats import chi2
import pandas as pd

from Utility import split_into_chunks


class FOAnalyzer:

    def analyze_results(self, smelling_co_changing_pairs, all_smelly_pairs, co_changed_pairs, all_pairs):
        # All pairs formed from all files changed in the relevant time frame.

        # Only keep the smelly pairs that are part of 'all_pairs'
        relevant_smelly_pairs = all_smelly_pairs.intersection(all_pairs)
        #relevant_smelly_pairs = [x for x in all_smelly_pairs if x in all_pairs]

        # Calculate sets for contingency table
        non_smelling_non_co_changing_pairs = all_pairs.difference(relevant_smelly_pairs).difference(co_changed_pairs)
        #non_smelling_non_co_changing_pairs = [x for x in all_pairs if x not in relevant_smelly_pairs and x not in co_changed_pairs]
        non_smelling_co_changing_pairs = co_changed_pairs.difference(relevant_smelly_pairs)
        #non_smelling_co_changing_pairs = [x for x in co_changed_pairs if x not in relevant_smelly_pairs]
        smelling_non_co_changing_pairs = relevant_smelly_pairs.difference(smelling_co_changing_pairs)
        #smelling_non_co_changing_pairs = [x for x in relevant_smelly_pairs if x not in smelling_co_changing_pairs]

        # Calculate values of the contingency table cells
        non_smelling_non_co_changing_pairs_size = len(non_smelling_non_co_changing_pairs)
        non_smelling_co_changing_pairs_size = len(non_smelling_co_changing_pairs)
        smelling_non_co_changing_pairs_size = len(smelling_non_co_changing_pairs)
        smelling_co_changing_pairs_size = len(smelling_co_changing_pairs)

        # total amount of observations
        n = non_smelling_non_co_changing_pairs_size + non_smelling_co_changing_pairs_size + smelling_non_co_changing_pairs_size + smelling_co_changing_pairs_size
        print("general information:")
        print("all changed pairs during the history: " + str(len(all_pairs)))
        print("smells in project: " + str(len(all_smelly_pairs)))
        print("smells contained in all pairs: " + str(len(relevant_smelly_pairs)))
        print("all co changes in project: " + str(len(co_changed_pairs)))
        print("\n")

        self.perform_chi2_analysis(non_smelling_non_co_changing_pairs_size, non_smelling_co_changing_pairs_size, smelling_non_co_changing_pairs_size, smelling_co_changing_pairs_size, n)
        self.perform_fisher(non_smelling_non_co_changing_pairs_size, non_smelling_co_changing_pairs_size, smelling_non_co_changing_pairs_size, smelling_co_changing_pairs_size)

    # Executes Fisher's test on the passed contingency table values.
    @staticmethod
    def perform_fisher(non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs):
        oddsratio, pvalue = stats.fisher_exact([[non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs], [smelling_non_co_changing_pairs, smelling_co_changing_pairs]])
        print("Fisher values:")
        print("oddsratio: " + str(oddsratio))
        print("p-value: " + str(pvalue))
        print("\n")

    # Executes the chi squared test on the passed contingency table values.
    def perform_chi2_analysis(self, non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs, n):
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
        print('oddsratio: %.6f' % self.odds_ratio(non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs))
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

    # Calculates the odds ratio on the passed contingency table values.
    @staticmethod
    def odds_ratio(non_smelling_non_co_changing_pairs, non_smelling_co_changing_pairs, smelling_non_co_changing_pairs, smelling_co_changing_pairs):
        if non_smelling_co_changing_pairs*smelling_non_co_changing_pairs == 0:
            return 0
        return (non_smelling_non_co_changing_pairs*smelling_co_changing_pairs)/(non_smelling_co_changing_pairs*smelling_non_co_changing_pairs)

    # Returns all co-changes that have a matching smell. Note: can contain duplicates.
    @staticmethod
    def get_co_changed_smelly_pairs(co_change_df, smell_df, level='file'):
        co_changes_smells = None  # Collects cumulative matches
        cc_chunks = split_into_chunks(co_change_df, 10000)  # df's with <= 1000 rows
        smell_chunks = split_into_chunks(smell_df, 10000)
        processed_chunks = []
        for cc_chunk in cc_chunks:
            for smell_chunk in smell_chunks:
                co_changes_smells_chunk = cc_chunk.merge(smell_chunk, how='inner', left_on=[level+'1', level+'2'], right_on=[level+'1', level+'2'])
                # Check we at least have a match
                if co_changes_smells_chunk.empty:
                    continue

                co_changes_smells_chunk = co_changes_smells_chunk[co_changes_smells_chunk['parsedStartDate'] <= co_changes_smells_chunk['parsedVersionDate']]
                co_changes_smells_chunk = co_changes_smells_chunk[co_changes_smells_chunk['parsedVersionDate'] <= co_changes_smells_chunk['parsedEndDate']]

                if co_changes_smells_chunk.empty:
                    continue

                processed_chunks.append(co_changes_smells_chunk)

        return pd.concat(processed_chunks)
