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