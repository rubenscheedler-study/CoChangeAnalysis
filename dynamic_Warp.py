from dtw import dtw
import pandas as pd

from helper_scripts.Commit_date_helper import convert_hashlist_to_datelist
from helper_scripts.components_helper import get_components


def perform_dtw():
    components = get_components()
    # group versions by name
    grouped_comp = components.groupby('name')['version'].apply(list).reset_index(name='changeVersions')
    # generate list of change dates from versions
    grouped_comp['changeMoments'] = list(map(convert_hashlist_to_datelist, grouped_comp['changeVersions']))

    return_list = []
    # iterate over rows
    for x in grouped_comp.itertuples():
        # drop rows we already had
        for y in grouped_comp.drop(grouped_comp.index[:x.Index + 1]).itertuples():
            if generate_dtw(x.changeMoments, y.changeMoments):
                return_list.append((x.name, y.name))

    warpdf = pd.DataFrame(return_list, columns=['file1', 'file2'])
    return warpdf, components['name']


def generate_dtw(x, y):
    dynamic_warp = dtw(x=x, y=y)
    return dynamic_warp.normalizedDistance < 86400
