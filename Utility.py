import datetime
from functools import reduce
from itertools import combinations

import pandas as pd

from config import input_directory, analysis_start_date, analysis_end_date


def read_filename_pairs(path_to_csv):
    all_pairs = pd.read_csv(path_to_csv)
    full_path_pairs = list(zip(all_pairs.file1, all_pairs.file2))
    return list(map(lambda pair: (map_path_to_filename(pair[0]), map_path_to_filename(pair[1])), full_path_pairs))

# Looks at {input}/{project}/smell-characteristics-consecOnly.csv
# Reads all pairs. Filters duplicates and filters out pairs outside the date range set in config.
def get_project_smells_in_range(ignore_inner_classes=True):
    smells = pd.read_csv(input_directory + "/smell-characteristics-consecOnly.csv")
    smells = smells[smells.affectedComponentType == "class"]
    # Add a column for the parsed version date.
    smells['parsedVersionDate'] = smells['versionDate'].map(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
    # filter rows on date range
    smells = smells[smells.apply(lambda row: analysis_start_date <= row['parsedVersionDate'] <= analysis_end_date, axis=1)]
    # Generate unique 2-sized combinations for each smell file list.
    # These are the smelly pairs since they share a code smell.
    ### non_unique_pairs = list(chain(*map(lambda files: combinations(files, 2), map(parse_affected_elements, smells_affected_elements))))
    # For now we filter duplicate incidents of pairs being contained in smells.
    ### smelly_pairs = set(non_unique_pairs)
    smell_rows = reduce(
            lambda a, b: pd.concat([a, b], ignore_index=True),  # Concat all smell sub-dfs into one big one.
            smells.apply(explode_row_into_pairs, axis=1)
    )
    # Map package.class to class
    smell_rows['file1'] = smell_rows['file1'].apply(lambda s: get_class_from_package(s, ignore_inner_classes))
    smell_rows['file2'] = smell_rows['file2'].apply(lambda s: get_class_from_package(s, ignore_inner_classes))

    return smell_rows


# Returns a DataFrame [file1, file2, parsedVersionDate]
def explode_row_into_pairs(row):
    # For this row (smell+version) see what files it affects.
    affected_files = parse_affected_elements(row.affectedElements)
    # Create a new row for each combination of two distinct files.
    file_pairs = combinations(affected_files, 2)
    file_pairs_with_date = list(map(lambda fp: fp+(row.parsedVersionDate,), file_pairs))

    # Define the dataframe to return
    return pd.DataFrame(file_pairs_with_date, columns=['file1', 'file2', 'parsedVersionDate'])


# Parses a string of the form [package.class$innerclass, package.class$innerclass, ...] to a list
def parse_affected_elements(affected_elements_list_string):
    return list(
            map(lambda p: p.split(".")[-1],  # map every package-file a.b.c to its file: c (last part)
                affected_elements_list_string[1:-1].split(", ")  # split the list into its distinct files
                )
        )


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


def sort_tuple_elements(tuple_list):
    return list(map(lambda t: (t[0], t[1]) if t[0] < t[1] else (t[1], t[0]), tuple_list))


# Swaps file1 and file2 if they are not in alphabetical order.
def order_file1_and_file2(df):
    return df.apply(lambda row: row if row.file1 < row.file2 else swap_file1_and_file2(row), axis=1)


def swap_file1_and_file2(row):
    file1_old = row.file1
    row.file1 = row.file2
    row.file2 = file1_old
    return row


# Joins the two data frames on file1 and file2 and returns distinct matching (file1, file2) tuples.
def get_intersecting_file_pairs(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    matched_df = df1.merge(df2, how='inner', left_on=['file1', 'file2'], right_on=['a', 'b'])
    matched_df = matched_df.drop(columns=['a', 'b'])
    return set(list(zip(matched_df.file1, matched_df.file2)))


def get_not_intersecting_file_pairs(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    not_matched_df = df1.merge(df2, how='left', left_on=['file1', 'file2'], right_on=['a', 'b'], indicator='i').query('i == "left_only"').drop('i', 1)
    not_matched_df = not_matched_df.drop(columns=['a', 'b'])
    return set(list(zip(not_matched_df.file1, not_matched_df.file2)))


def intersection_on_file_names(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    matched_df = df1.merge(df2, how='inner', left_on=['file1', 'file2'], right_on=['a', 'b'])
    matched_df = matched_df.drop(columns=['a', 'b'])
    return matched_df


def difference_on_file_names(df1, df2):
    df2 = df2.rename(columns={"file1": "a", "file2": "b"})
    not_matched_df = df1.merge(df2, how='left', left_on=['file1', 'file2'], right_on=['a', 'b'], indicator='i').query('i == "left_only"').drop('i', 1)
    not_matched_df = not_matched_df.drop(columns=['a', 'b'])
    return not_matched_df


def to_unique_file_tuples(df):
    return set(list(filter(lambda x: x[0] != x[1], zip(df.file1, df.file2))))