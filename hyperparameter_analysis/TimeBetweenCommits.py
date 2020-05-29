import matplotlib.pyplot as plt
import numpy as np

def time_between_commits(repo, branch):
    print("---- Time between commits ----")
    # Get all commits for this repo on the master branch.
    commits = list(repo.iter_commits(branch))
    # Calculate the time between commits in minutes
    commitDifs = [round((commits[i].committed_datetime.timestamp() - commits[i+1].committed_datetime.timestamp())/60) for i in range(len(commits)-1)]
    plt.hist(commitDifs, bins='auto')
    plt.title("Histogram committimedifference")
    plt.yscale("log")
    plt.show()

    firstquartile = np.percentile(commitDifs, 25)
    print("Q1: ", firstquartile," minutes")
    median = np.percentile(commitDifs, 50)
    print("Q2: ", median, " minutes")
    thirdquartile = np.percentile(commitDifs, 75)
    print("Q3: ", thirdquartile, " minutes")
