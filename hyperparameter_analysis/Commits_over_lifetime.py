def commits_over_lifetime(repo, branch):
    print("----General project info----")
    commits = list(repo.iter_commits(branch))
    lastdate = commits[0].committed_datetime.date()
    commits.reverse()
    firstdate = commits[0].committed_datetime.date()

    commitperDay = len(commits)/(lastdate-firstdate).days
    print("First commit date:", firstdate)
    print("Commits per day (average): ", commitperDay)
    print("Last commit date:", lastdate)
