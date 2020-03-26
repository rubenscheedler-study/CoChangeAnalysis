def commits_over_lifetime(repo):
    commits = list(repo.iter_commits('master'))
    lastdate = commits[0].committed_datetime.date()
    commits.reverse()
    firstdate = commits[0].committed_datetime.date()

    commitperDay = len(commits)/(lastdate-firstdate).days
    print(commitperDay)
