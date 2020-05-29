import os
import numpy as np

import pandas as pd


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
    df['package1'], df['package2'] = np.minimum(df['package1'], df['package2']), np.maximum(df['package1'],
                                                                                            df['package2'])
    return df


def to_unique_file_tuples(df):
    df = df.drop_duplicates(subset=['file1', 'file2'])
    return set(list(zip(df.file1, df.file2)))


def split_into_chunks(df, chunk_size):
    return [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]


def get_twin_tuples(lst):
    return [(x, x) for x in lst]


def read_or_create_csv(path_to_csv):
    if not os.path.isfile(path_to_csv):
        f = open(path_to_csv, "w+")
        f.close()

    return pd.read_csv(path_to_csv)
