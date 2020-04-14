from git import Repo

# Constants
from Commits_over_lifetime import commits_over_lifetime
from FilesPerCommit import files_per_commit_information
from TimeBetweenCommits import time_between_commits
from projects.ThresholdAnalysis import threshold_distribution

git_url = "https://github.com/apache/xerces2-j.git"
clone_directory = "projects/xerces2-j/"
branch = 'trunk'

# Clone the repo we want to analyse.
#Repo.clone_from(git_url, clone_directory)
repo = Repo(clone_directory)

# Analyse the amount of files per commit for this repo.
files_per_commit_information(repo, branch)

# Analyse the time between commits for this repo.
time_between_commits(repo, branch)

# Get the number of commits per day the repo exists
commits_over_lifetime(repo, branch)

# Histogram of thresholds (make sure to update cochanges.csv!)
threshold_distribution()