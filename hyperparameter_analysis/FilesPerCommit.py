import itertools
from functools import reduce

import matplotlib.pyplot as plt
import numpy as np


def files_per_commit_information(repo, branch):
    # Get all commits for this repo on the master branch.
    commits = list(repo.iter_commits(branch, max_count=1000))
    # For each commit determine the amount of files it affected.
    file_counts = list(map(lambda c: len(c.stats.files), commits))
    # Sort fileCounts ascending
    file_counts = sorted(file_counts)
    # Drop the highest 5 percent (outliers like folder moving operations)
    file_counts = file_counts[:len(file_counts)-(int(0.05*len(file_counts)))]

    # Results
    print("----results files per commit----")
    max_file_count = max(file_counts)
    print("Highest files affected count: ", max_file_count)
    print("Average files affected count: ", np.mean(file_counts))
    print("Median files affected count: ", np.median(file_counts))
    unique_file_count = count_unique_files(commits)
    print("Distinct files: ", unique_file_count)
    print("Average overlap: ", average_pure_co_change(commits,unique_file_count), " commits")
    # for every commit define A = files affected
    # calc A over 2

    plt.hist(file_counts, bins=range(0, max_file_count+1))
    plt.title("Histogram of files affected per commit")
    plt.show()


def count_unique_files(commits):
    list_of_file_lists = map(lambda c: c.stats.files.items(), commits)
    files = list(itertools.chain.from_iterable(list_of_file_lists))
    files = list(map(lambda t: t[0], files))
    #files = list(reduce(lambda a, b: a + b, )
    distinct_files = list(set(files))
    return len(distinct_files)

def average_pure_co_change(commits, unique_file_count):
    cochange_chances = []
    for c in commits:
        fileCount = len(c.stats.files)
        if fileCount == 1:  # no pure co-changes can be found
            cochange_chances.append(0)
        else:
            # Calculate the chance that a pair occurs in this commit.
            chance_on_pair = (fileCount/unique_file_count) * ((fileCount-1)/(unique_file_count-1))
            cochange_chances.append(chance_on_pair)

    # Determine the average per commit. Multiply with commit count to find min. threshold.
    return np.mean(cochange_chances) * len(commits)
