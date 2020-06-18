from github import Github

import config
from config import input_directory, api_key_github
import pandas as pd
from datetime import datetime

from helper_scripts.pickle_helper import load_pickle

g = Github(api_key_github)
repo = g.get_repo(config.git_repo)
versiondates_df = None
try:
    versiondates_df = pd.read_csv(config.output_directory + '/changeDates.csv', header=0, names=['key', 'value'])
except FileNotFoundError:
    pass
if versiondates_df is None:
    # get all version we have based on the smells with their date
    smell_pd = pd.read_csv(input_directory + "/smell-characteristics-consecOnly.csv")[['version', 'versionDate']]
    # convert to valid timestamp
    smell_pd['versionDatetime'] = list(
        map(lambda x: datetime.timestamp(datetime.strptime(x, '%d-%m-%Y')), smell_pd['versionDate']))
    smells = dict(zip(list(map(lambda x: x.split('-')[-1], smell_pd.version)), smell_pd.versionDatetime)) # remove split for component-characteristics
else:
    smells = dict(zip(versiondates_df['key'], versiondates_df['value'])) # remove split for component-characteristics
filechanges = []


def get_commit_date(commit_hash):
    # already in the smell version dictionary
    u = smells.get(commit_hash, None)
    if u is not None:
        return u
    else:
        # get from github then add to dictionary
        commit = repo.get_commit(sha=commit_hash)
        date = datetime.timestamp(commit.commit.committer.date)
        smells[commit_hash] = date
        pd_backup = pd.DataFrame.from_dict(smells, orient='index')
        pd_backup.to_csv(config.output_directory + '/changeDates.csv', header=False)
        return date


def convert_hashlist_to_datelist(hashlist):
    return list(map(get_commit_date, hashlist))


def add_file_dates(df):
    df[['startdate', 'enddate']] = df.apply(lambda x: get_date_window(x.file1, x.file2), axis = 1)
    return df


def get_date_window(file1, file2):
    file1_row = filechanges.loc[file1]
    file2_row = filechanges.loc[file2]
    first_moment = min(file1_row.mindate, file2_row.mindate)
    last_moment = max(file1_row.maxdate, file2_row.maxdate)
    x= pd.Series([datetime.fromtimestamp(first_moment), datetime.fromtimestamp(last_moment)])
    return x


def store_dates_for_files(df):
    # group versions by name
    grouped_comp = df.groupby('name')['version'].apply(list).reset_index(name='changeVersions')
    # generate list of change dates from versions
    grouped_comp['changeMoments'] = list(map(convert_hashlist_to_datelist, grouped_comp['changeVersions']))
    grouped_comp['mindate'] = list(map(min, grouped_comp['changeMoments']))
    grouped_comp['maxdate'] = list(map(max, grouped_comp['changeMoments']))
    grouped_comp = grouped_comp.set_index('name')
    global filechanges
    filechanges = grouped_comp.drop(['changeVersions', 'changeMoments'], axis=1)
