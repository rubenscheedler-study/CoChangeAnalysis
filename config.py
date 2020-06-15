import datetime
import getopt
import sys


analysis_start_date = datetime.datetime(2011, 7, 28)
analysis_end_date = datetime.datetime(2020, 5, 14)
project_name = "swagger-core"
input_directory = "input/" + project_name
output_directory = "output/" + project_name
clone_directory = "projects/" + project_name
git_repo = "swagger-api/" + project_name
git_url = "https://github.com/"+git_repo+".git"
branch = 'master'




api_key_github = 'a0b658d0dc9342b2fe5ba236ec4f2d5a29ef85dc'
git_project_owner = "unknown_owner"  # Only used for the command line initialization
results_file = "analysis_results.csv"


def initialize_config():
    #if __name__ == "__main__":
    #print("reading args!")
    # We are running from the command line. Overwrite the above config attributes with the values below
    read_args(sys.argv[1:])


# Reads arguments from the command line and sets their respective config attributes.
def read_args(argv):
    # Parse arguments
    try:
        opts, args = getopt.getopt(argv, "p:s:e:o:b:")
        print(opts)
    except getopt.GetoptError:
        print('<script_name>.py -p <project name> -s <start date dd-mm-yyyy> -e <end date dd-mm-yyyy> -o <owner of the project on git> -b <branch>')
        sys.exit(2)

    # Store arguments
    for opt, arg in opts:
        if opt == '-p':
            global project_name
            project_name = arg
            print(project_name)
        elif opt == '-s':
            global analysis_start_date
            analysis_start_date = datetime.datetime.strptime(arg, '%d-%m-%Y')
        elif opt == '-e':
            global analysis_end_date
            analysis_end_date = datetime.datetime.strptime(arg, '%d-%m-%Y')
        elif opt == '-o':
            global git_project_owner
            git_project_owner = arg
        elif opt == '-b':
            global branch
            branch = arg

    # Update computed properties
    global input_directory
    input_directory = "input/" + project_name
    global output_directory
    output_directory = "output/" + project_name
    global clone_directory
    clone_directory = "projects/" + project_name
    global git_repo
    git_repo = git_project_owner + "/" + project_name
    global git_url
    git_url = "https://github.com/" + git_repo + ".git"
