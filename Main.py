

from git import Repo
import pandas as pd
import config

# Constants
from ClassFOAnalysis import ClassFOAnalysis
from CommitsPerCommitDay import commits_per_commitday
from Commits_over_lifetime import commits_over_lifetime
from Exploration import run_exploration
from FilesPerCommit import files_per_commit_information
#from MBA import perform_mba
from TimeBetweenCommits import time_between_commits
from ThresholdAnalysis import threshold_distribution
from Utility import get_class_from_package
from config import output_directory
#from dynamic_Warp import perform_dtw
#from helper_scripts.Commit_date_helper import add_file_dates
#from helper_scripts.output_helper import filter_duplicate_file_pairs, generate_all_pairs


def hyper_param_analysis():
    from pathlib import Path
    clone_dir = Path(config.clone_directory)
    if not clone_dir.is_dir(): #exists
        # Clone the repo we want to analyse.
        Repo.clone_from(config.git_url, config.clone_directory)
    repo = Repo(config.clone_directory)

    # Analyse the amount of files per commit for this repo.
    files_per_commit_information(repo, config.branch)

    # Analyse the time between commits for this repo.
    time_between_commits(repo, config.branch)

    # Get the number of commits per day the repo exists
    commits_over_lifetime(repo, config.branch)

    # Get the number of commits per day on which there were commits
    commits_per_commitday(repo, config.branch)

#hyper_param_analysis()

threshold_distribution()

"""
warps, changedFiles = perform_dtw()

# Map changed files to class.java
changedFiles = list(map(get_class_from_package, changedFiles))

warpdf = filter_duplicate_file_pairs(warps)

all_pairs = generate_all_pairs(changedFiles)
warp_with_dates = add_file_dates(warpdf)

# Map warps to class.java
warp_with_dates['file1'] = warp_with_dates['file1'].apply(lambda f: get_class_from_package(f, False))
warp_with_dates['file2'] = warp_with_dates['file2'].apply(lambda f: get_class_from_package(f, False))

warp_with_dates.to_csv(output_directory + "/dtw.csv")
all_pairs.to_csv(output_directory + "/file_pairs_dtw.csv")

rules, changedFiles = perform_mba()
# Map changed files to class.java
changedFiles = list(map(get_class_from_package, changedFiles))

rules = filter_duplicate_file_pairs(rules)

all_pairs_mba = generate_all_pairs(changedFiles)
rules_with_dates = add_file_dates(rules)

# Map warps to class.java
rules_with_dates['file1'] = rules_with_dates['file1'].apply(lambda f: get_class_from_package(f, False))
rules_with_dates['file2'] = rules_with_dates['file2'].apply(lambda f: get_class_from_package(f, False))

rules_with_dates.to_csv(output_directory + "/mba.csv")
all_pairs_mba.to_csv(output_directory + "/file_pairs_mba.csv")

"""
#run_exploration()

#a = ClassFOAnalysis()
#a.execute()
