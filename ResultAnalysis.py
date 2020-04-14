import datetime

import numpy as np
import pandas as pd
from itertools import combinations, chain
from scipy import stats
from scipy.stats import chi2

def analyze_results():
    analysis_end_date = datetime.datetime(2019, 4, 6)
    analysis_start_date = datetime.datetime(2008, 5, 26)
    # All pairs formed from all files changed in the relevant time frame.
    all_pairs = sort_tuple_elements(find_all_pairs())
    # All smelly pairs of the whole history of the project.
    smelly_pairs = sort_tuple_elements(find_smelly_pairs(analysis_start_date, analysis_end_date))
    # Only keep the smelly pairs that are part of 'all_pairs'
    relevant_smelly_pairs = set(smelly_pairs).intersection(all_pairs)
    co_changed_pairs = sort_tuple_elements(find_co_changed_pairs())

    # Calculate sets for contingency table
    non_smelling_non_co_changing_pairs = set(all_pairs).difference(relevant_smelly_pairs).difference(co_changed_pairs)
    non_smelling_co_changing_pairs = set(co_changed_pairs).difference(relevant_smelly_pairs)
    smelling_non_co_changing_pairs = set(relevant_smelly_pairs).difference(co_changed_pairs)
    smelling_co_changing_pairs = set(relevant_smelly_pairs).intersection(co_changed_pairs)

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


def find_co_changed_pairs():
    co_changed_pairs = pd.read_csv("input/cochanges.csv")
    return list(zip(co_changed_pairs.file1, co_changed_pairs.file2))


def find_all_pairs():
    all_pairs = pd.read_csv("input/file_pairs.csv")
    full_path_pairs = list(zip(all_pairs.file1, all_pairs.file2))
    return list(map(lambda pair: (map_path_to_filename(pair[0]), map_path_to_filename(pair[1])), full_path_pairs))


def find_smelly_pairs(analysis_start_date, analysis_end_date):
    smells = pd.read_csv("input/smell-characteristics-consecOnly.csv")
    smells = smells[smells.affectedComponentType == "class"]
    # Add a column for the parsed version date.
    smells['parsedVersionDate'] = smells['versionDate'].map(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
    # filter rows on date range
    smells = smells[analysis_start_date <= smells.parsedVersionDate <= analysis_end_date]
    smells_affected_elements = smells.affectedElements
    # Generate unique 2-sized combinations for each smell file list.
    # These are the smelly pairs since they share a code smell.
    non_unique_pairs = list(chain(*map(lambda files: combinations(files, 2), map(parse_affected_elements, smells_affected_elements))))
    # For now we filter duplicate incidents of pairs being contained in smells.
    smelly_pairs = set(non_unique_pairs)
    return smelly_pairs


# Parses a string of the form [a.java, b.java, ...]
def parse_affected_elements(affected_elements_list_string):
    return list(map(
        lambda f: f + ".java",  # finally, add .java to each filename f
        map(lambda p: p.split(".")[-1],  # map every package-file a.b.c to its file: c (last part)
            affected_elements_list_string[1:-1].split(", ")  # split the list into its distinct files
            )
        )
    )


def map_path_to_filename(path):
    return path.split("/")[-1]


def sort_tuple_elements(tuple_list):
    return list(map(lambda t: (t[0], t[1]) if t[0] < t[1] else (t[1], t[0]), tuple_list))


analyze_results()
