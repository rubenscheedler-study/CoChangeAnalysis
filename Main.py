from git import Repo
from FilesPerCommit import files_per_commit_information

# Constants
git_url = "https://github.com/swagger-api/swagger-core.git";
clone_directory = "projects/swagger-core/"

# Clone the repo we want to analyse.
#Repo.clone_from(git_url, clone_directory)
repo = Repo(clone_directory)

# Analyse the amount of files per commit for this repo.
files_per_commit_information(repo)


