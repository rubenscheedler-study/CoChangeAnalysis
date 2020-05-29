import numpy as np
import pandas as pd


def sort_tuple_elements(tuple_list):
    return list(map(lambda t: (t[0], t[1]) if t[0] < t[1] else (t[1], t[0]), tuple_list))


def filter_duplicate_file_pairs(dataframe):
    result = sort_tuple_elements(list(zip(dataframe.file1, dataframe.file2)))
    result = set(result)
    return pd.DataFrame(result, columns=['file1', 'file2'])


def generate_all_pairs(changedFiles):
    unique_values = pd.unique(changedFiles)
    return_list = []
    for i, x in enumerate(unique_values):
        # drop rows we already had
        for j, y in enumerate(unique_values[i+1:]):
            return_list.append((x, y))
    return pd.DataFrame(return_list, columns=['file1', 'file2'])

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


def find_pairs(path_to_csv):
    co_changed_pairs = pd.read_csv(path_to_csv)
    return co_changed_pairs