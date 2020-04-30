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
def get_project_smells_in_range():
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