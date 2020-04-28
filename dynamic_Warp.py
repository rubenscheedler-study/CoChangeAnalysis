from datetime import datetime

from dtw import dtw, dtwPlot
import pandas as pd
from github import Github

g = Github('a0b658d0dc9342b2fe5ba236ec4f2d5a29ef85dc')
repo = g.get_repo("apache/xerces2-j")
# get all version we have based on the smells with their date
smellpd = pd.read_csv("input/smell-characteristics-consecOnly.csv")[['version', 'versionDate']]
# convert to valid timestamp
smellpd['versionDatetime'] = list(map(lambda x: datetime.timestamp(datetime.strptime(x, '%d-%m-%Y')), smellpd['versionDate']))
smells = dict(zip(smellpd.version, smellpd.versionDatetime))


def perform_dtw():
    components = pd.read_csv("input/component-characteristics-consecOnly.csv")
    # only consider classes, not packages
    orgcomponents = components[components['type'] == 'class']
    # filter on added or changed
    componentsZero = orgcomponents[orgcomponents['changeHasOccurredMetric'] == '0']
    componentsTrue = orgcomponents[orgcomponents['changeHasOccurredMetric'] == True]
    components = componentsZero.append(componentsTrue, ignore_index=True)
    length = len(components.index)
    components = components[['version', 'name']]
    # group versions by name
    grouped_comp = components.groupby('name')['version'].apply(list).reset_index(name='changeVersions')
    # generate list of change dates from versions
    grouped_comp['changeMoments'] = list(map(convert_hashlist_to_datelist, grouped_comp['changeVersions']))
    count = 0
    # iterate over rows
    for x in grouped_comp.itertuples():
        # drop rows we already had
        for y in grouped_comp.drop(grouped_comp.index[:x.Index + 1]).itertuples():
            if generate_dtw(x.changeMoments, y.changeMoments):
                yield (x.name, y.name)

    print(count)


def convert_hashlist_to_datelist(hashlist):
    return list(map(get_commit_date, hashlist))


def get_commit_date(commithash):
    # already in the smell version dictionary
    u = smells.get(commithash, None)
    if u is not None:
        return u
    else:
        # get from github then add to dictionary
        commit = repo.get_commit(sha=commithash)
        date = datetime.timestamp(commit.commit.committer.date)
        smells[commithash] = date
        return date


def generate_dtw(x, y):
    dynamic_warp = dtw(x=x, y=y)
    if dynamic_warp.normalizedDistance < 86400:
        print(dynamic_warp.normalizedDistance)

    return dynamic_warp.normalizedDistance < 86400
