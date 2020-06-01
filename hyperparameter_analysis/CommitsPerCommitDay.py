from collections import defaultdict

import seaborn
import matplotlib.pyplot as plt


def commits_per_commitday(repo, branch):
    commits = list(repo.iter_commits(branch))
    commitWithDate = list(map(lambda x: (x.committed_datetime.date(), x), commits))
    d = defaultdict(list)
    for key, val in commitWithDate:
        d[key] = d.get(key, 0) + 1

    print("Commits per commit day: ", sum(d.values())/len(d))

    seaborn.violinplot(list(d.values()))
    plt.title("Violin boxplot of commit per day in which there were commits")
    plt.show()