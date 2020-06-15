import numpy as np
import pandas as pd

from helper_scripts.Commit_date_helper import add_file_dates
from helper_scripts.smell_helper import get_class_from_package


def sort_tuple_elements(tuple_list):
    return list(map(lambda t: (t[0], t[1]) if t[0] < t[1] else (t[1], t[0]), tuple_list))


def filter_duplicate_file_pairs(dataframe):
    result = sort_tuple_elements(list(zip(dataframe.file1, dataframe.file2)))
    result = set(result)
    return pd.DataFrame(result, columns=['file1', 'file2'])

# Swaps file1 and file2 if they are not in alphabetical order.
def order_file1_and_file2(df):
    df['file1'], df['file2'] = np.minimum(df['file1'], df['file2']), np.maximum(df['file1'], df['file2'])
    return df


# Swaps package1 and package1 if they are not in alphabetical order.
def order_package1_and_package2(df):
    df['package1'], df['package2'] = np.minimum(df['package1'], df['package2']), np.maximum(df['package1'],
                                                                                            df['package2'])
    return df


def to_unique_file_tuples(df):
    df = df.drop_duplicates(subset=['file1', 'file2'])
    return set(list(zip(df.file1, df.file2)))


def find_pairs_with_date_range(path_to_csv, dateformat):
    co_changed_pairs_with_date_range = pd.read_csv(path_to_csv)
    co_changed_pairs_with_date_range['parsedStartDate'] = pd.to_datetime(co_changed_pairs_with_date_range['startdate'],
                                                                         format=dateformat)
    co_changed_pairs_with_date_range['parsedEndDate'] = pd.to_datetime(co_changed_pairs_with_date_range['enddate'],
                                                                       format=dateformat)
    return co_changed_pairs_with_date_range


def add_info_to_cochanges(df, changed_files):
    df = filter_duplicate_file_pairs(df)  # df: file1, file2

    # Add package columns
    df_with_dates = add_file_dates(df)

    df_with_dates = df_with_dates.merge(changed_files, how='inner', left_on=['file1'], right_on=['name'])
    df_with_dates = df_with_dates.drop(columns=['name'])
    df_with_dates = df_with_dates.rename(columns={'package': 'package1'})
    df_with_dates = df_with_dates.merge(changed_files, how='inner', left_on=['file2'], right_on=['name'])
    df_with_dates = df_with_dates.rename(columns={'package': 'package2'})
    df_with_dates = df_with_dates.drop(columns=['name'])
    # Map files to class.java
    df_with_dates['file1'] = df_with_dates['file1'].apply(get_class_from_package)
    df_with_dates['file2'] = df_with_dates['file2'].apply(get_class_from_package)
    return df_with_dates
