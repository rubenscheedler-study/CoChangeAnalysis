import matplotlib.pyplot as plt
import numpy as np

def time_between_commits(repo):
    # Get all commits for this repo on the master branch.
    commits = list(repo.iter_commits('master'))
    # Calculate the time between commits in minutes
    commitDifs = [round((commits[i].committed_datetime.timestamp() - commits[i+1].committed_datetime.timestamp())/60) for i in range(len(commits)-1)]
    plt.hist(commitDifs, bins='auto')
    plt.title("Histogram committimedifference")
    plt.show()

    firstquartile = np.percentile(commitDifs, 25)
    median = np.percentile(commitDifs, 50)
    thirdquartile = np.percentile(commitDifs, 75)

    print(firstquartile, median, thirdquartile)
