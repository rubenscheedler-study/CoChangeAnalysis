
from github import Github
from config import input_directory
import pandas as pd
from datetime import datetime

g = Github('a0b658d0dc9342b2fe5ba236ec4f2d5a29ef85dc')
repo = g.get_repo("SonarSource/sonarlint-intellij")
# get all version we have based on the smells with their date
smell_pd = pd.read_csv(input_directory + "/smell-characteristics-consecOnly.csv")[['version', 'versionDate']]
# convert to valid timestamp
smell_pd['versionDatetime'] = list(map(lambda x: datetime.timestamp(datetime.strptime(x, '%d-%m-%Y')), smell_pd['versionDate']))
smells = dict(zip(smell_pd.version, smell_pd.versionDatetime))

def convert_hashlist_to_datelist(hashlist):
    return list(map(get_commit_date, hashlist))

def get_commit_date(commit_hash):
    # already in the smell version dictionary
    u = smells.get(commit_hash, None)
    if u is not None:
        return u
    else:
        # get from github then add to dictionary
        commit = repo.get_commit(sha=commit_hash.split('-')[-1])
        date = datetime.timestamp(commit.commit.committer.date)
        smells[commit_hash] = date
        return date
