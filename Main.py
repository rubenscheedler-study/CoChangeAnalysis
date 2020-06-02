from git import Repo
import config

# Constants
from MBA import generate_mba_analysis_files
from hyperparameter_analysis.CommitsPerCommitDay import commits_per_commitday
from hyperparameter_analysis.Commits_over_lifetime import commits_over_lifetime
from Exploration import run_exploration
from hyperparameter_analysis.FilesPerCommit import files_per_commit_information
from hyperparameter_analysis.TimeBetweenCommits import time_between_commits
from dynamic_Warp import generate_dtw_analysis_files
from results_analysis.analysis import result_analysis


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


def generate_analysis():
    generate_dtw_analysis_files()
    generate_mba_analysis_files()

# hyper_param_analysis()
# threshold_distribution()
# generate_analysis()

run_exploration()

#result_analysis()

#start = time.time()
#run_exploration()
#end = time.time()
#print(end - start, " seconds elapsed")

