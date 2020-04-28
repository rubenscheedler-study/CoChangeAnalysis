from git import Repo
import pandas as pd

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
warps = perform_dtw()
warpdf = pd.DataFrame(warps, columns=['file1', 'file2'])
warpdf.to_csv("output/dtw.csv")


# warps = perform_dtw()
rules = perform_mba()

rules.to_csv("output/mba.csv")

# Clone the repo we want to analyse.
# Repo.clone_from(git_url, clone_directory)
# repo = Repo(clone_directory)

# Analyse the amount of files per commit for this repo.
#files_per_commit_information(repo, branch)

# Analyse the time between commits for this repo.
#time_between_commits(repo, branch)

# Get the number of commits per day the repo exists
#commits_over_lifetime(repo, branch)

# Histogram of thresholds (make sure to update cochanges.csv!)
#threshold_distribution()
# Get the number of commits per day on which there were commits
#commits_per_commitday(repo, branch)
