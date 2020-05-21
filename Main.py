

from git import Repo
import pandas as pd
import config

# Constants
from ClassFOAnalysis import ClassFOAnalysis
from CombinedFOAnalysis import CombinedFOAnalysis
from PackageFOAnalysis import PackageFOAnalysis
from CommitsPerCommitDay import commits_per_commitday
from Commits_over_lifetime import commits_over_lifetime
from Exploration import run_exploration
from FilesPerCommit import files_per_commit_information
#from MBA import generate_mba_analysis_files
from TimeBetweenCommits import time_between_commits
#from dynamic_Warp import generate_dtw_analysis_files


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


# threshold_distribution()


# generate_dtw_analysis_files()


# generate_mba_analysis_files()


# run_exploration()

cfa = ClassFOAnalysis()
cfa.execute()

pfa = PackageFOAnalysis()
pfa.execute()

comfa = CombinedFOAnalysis()
comfa.execute()
