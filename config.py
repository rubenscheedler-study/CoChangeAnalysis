import datetime

analysis_start_date = datetime.datetime(2011, 5, 11)
analysis_end_date = datetime.datetime(2020, 5, 14)
project_name = "guava"
input_directory = "input/" + project_name
output_directory = "output/" + project_name
clone_directory = "projects/" + project_name
git_repo = "google/" + project_name
git_url = "https://github.com/"+git_repo+".git"
branch = 'master'
