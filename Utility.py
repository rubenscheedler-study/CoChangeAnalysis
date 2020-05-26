import datetime
from functools import reduce
from itertools import combinations
import numpy as np

import pandas as pd

from config import input_directory, analysis_start_date, analysis_end_date
from helper_scripts.pickle_helper import load_pickle, save_pickle


def read_filename_pairs(path_to_csv):
    all_pairs = pd.read_csv(path_to_csv)
    full_path_pairs = list(zip(all_pairs.file1, all_pairs.file2))
    return pd.DataFrame(list(map(lambda pair: (map_path_to_filename(pair[0]), map_path_to_filename(pair[1])), full_path_pairs)), columns=['file1', 'file2'])


def find_pairs_with_date_range(path_to_csv, dateformat):
    co_changed_pairs_with_date_range = pd.read_csv(path_to_csv)
    co_changed_pairs_with_date_range['parsedStartDate'] = pd.to_datetime(co_changed_pairs_with_date_range['startdate'], format=dateformat)
    co_changed_pairs_with_date_range['parsedEndDate'] = pd.to_datetime(co_changed_pairs_with_date_range['enddate'], format=dateformat)
    return co_changed_pairs_with_date_range


def find_pairs(path_to_csv):
    co_changed_pairs = pd.read_csv(path_to_csv)
    return co_changed_pairs


#
# Code for class smells
#

# Looks at {input}/{project}/smell-characteristics-consecOnly.csv
# Reads all pairs. Filters duplicates and filters out pairs outside the date range set in config.
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


# Returns a DataFrame [file1, file2, parsedVersionDate]
def explode_row_into_class_pairs(row):
    # For this row (smell+version) see what files it affects.
    # Create a new row for each combination of two distinct files.
    file_pairs = combinations(row.affectedElementsList, 2)
    df = pd.DataFrame(file_pairs, columns=['file1', 'file2'])
    df = df.assign(parsedVersionDate=row.parsedVersionDate)
    return df


# Parses a string of the form [package.class$innerclass, package.class$innerclass, ...] to a list
def parse_affected_classes(affected_elements_list_string):
    return [i.split('.')[-1] for i in affected_elements_list_string.split(', ')]


#
# Code for package smells
#


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

    # pickle for later reuse
    save_pickle(smell_rows, "package_smells")

    return smell_rows


# Returns a DataFrame [file1, file2, parsedVersionDate]
def explode_row_into_package_pairs(row):
    # For this row (smell+version) see what packages it affects.
    affected_packages = parse_affected_packages(row.affectedElements)
    # Create a new row for each combination of two distinct packages.
    package_pairs = combinations(affected_packages, 2)
    df = pd.DataFrame(package_pairs, columns=['package1', 'package2'])
    df = df.assign(parsedVersionDate=row.parsedVersionDate)
    return df


# Removes the [...] and splits the inner content on comma to get the list of packages.
def parse_affected_packages(affected_elements_list_string):
    return affected_elements_list_string.split(", ")


def sort_tuple_elements(tuple_list):
    return list(map(lambda t: (t[0], t[1]) if t[0] < t[1] else (t[1], t[0]), tuple_list))


# Parses package.package.class$innerclass(.java) to either class or class$innerclass(.java)
def get_class_from_package(package_file_path, ignore_inner_classes=True):
    package_file_path = map_path_to_filename(package_file_path)
    raw_class_name = package_file_path

    if "." in package_file_path:
        if package_file_path.split(".")[-1] == "java":
            raw_class_name = package_file_path.split(".")[-2]
        else:
            raw_class_name = package_file_path.split(".")[-1]

    if ignore_inner_classes and "$" in raw_class_name:
        raw_class_name = raw_class_name.split("$")[0]
    return raw_class_name + ".java"


def map_path_to_filename(path):
    return path.split("/")[-1]


# Swaps file1 and file2 if they are not in alphabetical order.
def order_file1_and_file2(df):
    df['file1'], df['file2'] = np.minimum(df['file1'], df['file2']), np.maximum(df['file1'], df['file2'])
    return df


# Swaps package1 and package1 if they are not in alphabetical order.
def order_package1_and_package2(df):
    df['package1'], df['package2'] = np.minimum(df['package1'], df['package2']), np.maximum(df['package1'], df['package2'])
    return df


# Joins the two data frames on file1 and file2 and returns distinct matching (file1, file2) tuples.
def get_intersecting_file_pairs(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    matched_df = df1.merge(df2, how='inner', left_on=['file1', 'file2'], right_on=['a', 'b'])
    matched_df = matched_df.drop(columns=['a', 'b'])
    return set(list(zip(matched_df.file1, matched_df.file2)))


def get_not_intersecting_file_pairs(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    not_matched_df = df1.merge(df2, how='left', left_on=['file1', 'file2'], right_on=['a', 'b'], indicator='i').query(
        'i == "left_only"').drop('i', 1)
    not_matched_df = not_matched_df.drop(columns=['a', 'b'])
    return set(list(zip(not_matched_df.file1, not_matched_df.file2)))


def intersection_on_file_names(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    matched_df = df1.merge(df2, how='inner', left_on=['file1', 'file2'], right_on=['a', 'b'])
    matched_df = matched_df.drop(columns=['a', 'b'])
    return matched_df


def difference_on_file_names(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    not_matched_df = df1.merge(df2, how='left', left_on=['file1', 'file2'], right_on=['a', 'b'], indicator='i').query(
        'i == "left_only"').drop('i', 1)
    not_matched_df = not_matched_df.drop(columns=['a', 'b'])
    return not_matched_df


def to_unique_file_tuples(df):
    df = df.drop_duplicates(subset=['file1', 'file2'])
    return set(list(zip(df.file1, df.file2)))


def to_distinct_package_tuples(df):
    return set(zip(df.package1, df.package2))


def split_into_chunks(df, chunk_size):
    return [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]


def get_twin_tuples(lst):
    return [(x, x) for x in lst]

