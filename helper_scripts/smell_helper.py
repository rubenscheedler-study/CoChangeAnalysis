from itertools import combinations

import pandas as pd

# Looks at {input}/{project}/smell-characteristics-consecOnly.csv
# Reads all pairs. Filters duplicates and filters out pairs outside the date range set in config.
from Utility import get_class_from_package, get_twin_tuples
from config import input_directory, analysis_end_date, analysis_start_date
from helper_scripts.pickle_helper import load_pickle, save_pickle


def get_project_class_smells_in_range():
    class_smells = load_pickle("class_smells")
    if class_smells is not None:
        return class_smells

    smells = pd.read_csv(input_directory + "/smell-characteristics-consecOnly.csv")
    smells = smells[smells.affectedComponentType == "class"]

    # todo: this needs to be a function, as it is duplicated with the package version

    # Add a column for the parsed version date.
    smells['parsedVersionDate'] = pd.to_datetime(smells['versionDate'], format='%d-%m-%Y')
    # filter rows on date range
    smells = smells[smells['parsedVersionDate'] <= analysis_end_date]
    smells = smells[analysis_start_date <= smells['parsedVersionDate']]

    smells = smells[smells['affectedElements'] != '[]']
    smells['affectedElements'] = smells['affectedElements'].str[1:-1]

    # Generate unique 2-sized combinations for each smell file list.
    # These are the smelly pairs since they share a code smell.

    # split into a list (,) and strip the package from each file in that list (.)
    smells['affectedElementsList'] = [[x.split('.')[-1] for x in i] for i in smells['affectedElements'].str.split(', ')]
    # generate all combinations of affected files from that list
    smells['affectedElementCombinations'] = [list(combinations(i, 2)) for i in smells['affectedElementsList']]
    # drop the columns we dont need
    smells = smells[['affectedElementCombinations', 'parsedVersionDate']]
    # explode the list of combinations into multiple rows
    smells = smells.explode('affectedElementCombinations')
    # split the combination tuples into two columns
    smells[['file1', 'file2']] = pd.DataFrame(smells['affectedElementCombinations'].tolist(), index=smells.index)
    # The file can contain smells affecting just one file, which ends up resolving to nan. Luckily, they are not relevant so we filter them.
    smell_rows = smells.dropna()
    # Map package.class to class
    smell_rows['file1'] = smell_rows['file1'].apply(get_class_from_package)
    smell_rows['file2'] = smell_rows['file2'].apply(get_class_from_package)

    # pickle for later reuse
    save_pickle(smell_rows, "class_smells")

    return smell_rows

# Looks at {input}/{project}/smell-characteristics-consecOnly.csv
# Reads all pairs. Filters duplicates and filters out pairs outside the date range set in config.
def get_project_package_smells_in_range():
    package_smells = load_pickle("package_smells")
    if package_smells is not None:
        return package_smells

    smells = pd.read_csv(input_directory + "/smell-characteristics-consecOnly.csv")
    smells = smells[smells.affectedComponentType == "package"]

    # Add a column for the parsed version date.
    smells['parsedVersionDate'] = pd.to_datetime(smells['versionDate'], format='%d-%m-%Y')
    # filter rows on date range
    smells = smells[smells['parsedVersionDate'] <= analysis_end_date]
    smells = smells[analysis_start_date <= smells['parsedVersionDate']]

    smells = smells[smells['affectedElements'] != '[]']
    smells['affectedElements'] = smells['affectedElements'].str[1:-1]

    # Generate unique 2-sized combinations for each smell file list.
    # These are the smelly pairs since they share a code smell.

    # split into a list (,) and strip the package from each file in that list (.)
    smells['affectedPackagesList'] = smells['affectedElements'].str.split(', ')
    # generate all combinations of affected files from that list
    smells['affectedPackageCombinations'] = [list(combinations(i, 2)) + get_twin_tuples(i) for i in smells['affectedPackagesList']]
    # drop the columns we dont need
    smells = smells[['affectedPackageCombinations', 'parsedVersionDate']]
    # explode the list of combinations into multiple rows
    smells = smells.explode('affectedPackageCombinations')
    # split the combination tuples into two columns
    smells[['package1', 'package2']] = pd.DataFrame(smells['affectedPackageCombinations'].tolist(), index=smells.index)
    # The file can contain smells affecting just one file, which ends up resolving to nan. Luckily, they are not relevant so we filter them.
    smell_rows = smells.dropna()
    smell_rows = smell_rows.drop_duplicates()
    # pickle for later reuse
    save_pickle(smell_rows, "package_smells")

    return smell_rows