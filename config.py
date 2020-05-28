import datetime

analysis_start_date = datetime.datetime(2014, 8, 14)
analysis_end_date = datetime.datetime(2020, 5, 14)
project_name = "cassandra"
input_directory = "input/" + project_name
output_directory = "output/" + project_name
clone_directory = "projects/" + project_name
git_repo = "apache/" + project_name
git_url = "https://github.com/"+git_repo+".git"
branch = 'trunk'
