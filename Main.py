from git import Repo
import pandas as pd
import numpy as np

# Constants
from CommitsPerCommitDay import commits_per_commitday
from Commits_over_lifetime import commits_over_lifetime
from FilesPerCommit import files_per_commit_information
from MBA import perform_mba
from TimeBetweenCommits import time_between_commits
from ThresholdAnalysis import threshold_distribution
from dynamic_Warp import perform_dtw

git_url = "https://github.com/SonarSource/sonarlint-intellij.git"
clone_directory = "projects/sonarlint-intellij/"
branch = 'master'

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

warps, changedFiles = perform_dtw()
warpdf = pd.DataFrame(warps, columns=['file1', 'file2'])
warpdf = filter_duplicate_file_pairs(warpdf)
all_pairs = generate_all_pairs(changedFiles)
warpdf.to_csv("output/dtw.csv")
all_pairs.to_csv("output/file_pairs_dtw.csv")


rules, changedFiles = perform_mba()
rules['file1'] = list(map(lambda x: next(iter(x)), rules['antecedents']))
rules['file2'] = list(map(lambda x: next(iter(x)), rules['consequents']))
rules = filter_duplicate_file_pairs(rules)
all_pairs_mba = generate_all_pairs(changedFiles)
# both ante en consequents are sets of length 1

rules.to_csv("output/mba.csv")
all_pairs_mba.to_csv("output/file_pairs_mba.csv")

# Clone the repo we want to analyse.
# Repo.clone_from(git_url, clone_directory)
# repo = Repo(clone_directory)

# Analyse the amount of files per commit for this repo.
# files_per_commit_information(repo, branch)

# Analyse the time between commits for this repo.
# time_between_commits(repo, branch)

# Get the number of commits per day the repo exists
# commits_over_lifetime(repo, branch)

# Histogram of thresholds (make sure to update cochanges.csv!)
# threshold_distribution()
# Get the number of commits per day on which there were commits
# commits_per_commitday(repo, branch)
