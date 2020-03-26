import matplotlib.pyplot as plt
import numpy as np

def files_per_commit_information(repo):
    # Get all commits for this repo on the master branch.
    commits = list(repo.iter_commits('master'))
    # For each commit determine the amount of files it affected.
    fileCounts = list(map(lambda c: len(c.stats.files), commits))
    plt.hist(fileCounts, bins='auto')
    plt.title("Histogram with 'auto' bins")
    plt.show()



