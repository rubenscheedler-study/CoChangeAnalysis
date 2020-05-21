import datetime
from functools import reduce
from itertools import combinations
import numpy as np

import pandas as pd

from config import input_directory, analysis_start_date, analysis_end_date


def read_filename_pairs(path_to_csv):
    all_pairs = pd.read_csv(path_to_csv)
    full_path_pairs = list(zip(all_pairs.file1, all_pairs.file2))
    return pd.DataFrame(list(map(lambda pair: (map_path_to_filename(pair[0]), map_path_to_filename(pair[1])), full_path_pairs)), columns=['file1', 'file2'])

def find_pairs_with_date_range(path_to_csv, dateformat):
    co_changed_pairs_with_date_range = pd.read_csv(path_to_csv)
    co_changed_pairs_with_date_range['parsedStartDate'] = pd.to_datetime(co_changed_pairs_with_date_range['startdate'], format= dateformat)
    co_changed_pairs_with_date_range['parsedEndDate'] = pd.to_datetime(co_changed_pairs_with_date_range['enddate'], format= dateformat)
    return co_changed_pairs_with_date_range

def find_pairs(path_to_csv):
    co_changed_pairs = pd.read_csv(path_to_csv)
    return co_changed_pairs

#
# Code for class smells
#

# Looks at {input}/{project}/smell-characteristics-consecOnly.csv
# Reads all pairs. Filters duplicates and filters out pairs outside the date range set in config.
def get_project_class_smells_in_range(ignore_inner_classes=True):
    smells = pd.read_csv(input_directory + "/smell-characteristics-consecOnly.csv")
    smells = smells[smells.affectedComponentType == "class"]
    # Add a column for the parsed version date.

    smells['parsedVersionDate'] = pd.to_datetime(smells['versionDate'], format='%d-%m-%Y')
    # filter rows on date range
    smells = smells[smells['parsedVersionDate'] <= analysis_end_date]
    smells = smells[analysis_start_date <= smells['parsedVersionDate']]

    smells = smells[smells['affectedElements'] != '[]']
    smells['affectedElements'] = smells['affectedElements'].str[1:-1]

    # Generate unique 2-sized combinations for each smell file list.
    # These are the smelly pairs since they share a code smell.
    ### non_unique_pairs = list(chain(*map(lambda files: combinations(files, 2), map(parse_affected_elements, smells_affected_elements))))
    # For now we filter duplicate incidents of pairs being contained in smells.
    ### smelly_pairs = set(non_unique_pairs)
    dfs = []  # (file1, file2, date)

    for index, row in smells.iterrows():
        dfs.append(explode_row_into_class_pairs(row))

    smell_rows = pd.concat(dfs)
    """
    smell_rows = reduce(
        lambda a, b: pd.concat([a, b], ignore_index=True),  # Concat all smell sub-dfs into one big one.
        smells.apply(explode_row_into_class_pairs, axis=1)
    )
    """
    # Map package.class to class
    smell_rows['file1'] = smell_rows['file1'].apply(get_class_from_package)
    smell_rows['file2'] = smell_rows['file2'].apply(get_class_from_package)

    return smell_rows


# Returns a DataFrame [file1, file2, parsedVersionDate]
def explode_row_into_class_pairs(row):
    # For this row (smell+version) see what files it affects.
    affected_files = parse_affected_classes(row.affectedElements)
    # Create a new row for each combination of two distinct files.
    file_pairs = combinations(affected_files, 2)
    df = pd.DataFrame(file_pairs, columns=['file1', 'file2'])
    df.assign(parsedVersionDate=row.parsedVersionDate)
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
    smells = pd.read_csv(input_directory + "/smell-characteristics-consecOnly.csv")
    smells = smells[smells.affectedComponentType == "package"]
    # Add a column for the parsed version date.
    smells['parsedVersionDate'] = pd.to_datetime(smells['versionDate'], format='%d-%m-%Y')
    # filter rows on date range
    smells = smells[smells['parsedVersionDate'] <= analysis_end_date]
    smells = smells[analysis_start_date <= smells['parsedVersionDate']]

    smell_rows = reduce(
        lambda a, b: pd.concat([a, b], ignore_index=True),  # Concat all smell sub-dfs into one big one.
        smells.apply(explode_row_into_package_pairs, axis=1)
    )

    return smell_rows


# Returns a DataFrame [file1, file2, parsedVersionDate]
def explode_row_into_package_pairs(row):
    # For this row (smell+version) see what packages it affects.
    affected_packages = parse_affected_packages(row.affectedElements)
    # Create a new row for each combination of two distinct packages.
    package_pairs = combinations(affected_packages, 2)
    package_pairs_with_date = list(map(lambda fp: fp + (row.parsedVersionDate,), package_pairs))

    # Define the dataframe to return
    return pd.DataFrame(package_pairs_with_date, columns=['package1', 'package2', 'parsedVersionDate'])


# Removes the [...] and splits the inner content on comma to get the list of packages.
def parse_affected_packages(affected_elements_list_string):
    return affected_elements_list_string[1:-1].split(", ")


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
    return set(list(filter(lambda x: x[0] != x[1], zip(df.file1, df.file2))))


def to_unique_package_tuples(df):
    return set(list(filter(lambda x: x[0] != x[1], zip(df.package1, df.package2))))
