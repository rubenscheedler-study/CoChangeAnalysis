import os
from collections import namedtuple
from operator import attrgetter

import seaborn
from dtw import dtw
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import config
from MBA import print_quartiles
from config import output_directory
from helper_scripts.Commit_date_helper import convert_hashlist_to_datelist
from helper_scripts.changes_helper import get_changes
from helper_scripts.file_pair_helper import add_info_to_cochanges


def perform_dtw():
    components = get_changes()
    # group versions by name
    grouped_comp = components.groupby('name')['version'].apply(list).reset_index(name='changeVersions')
    # generate list of change dates from versions
    grouped_comp['changeMoments'] = list(map(convert_hashlist_to_datelist, grouped_comp['changeVersions']))

    Distance = namedtuple('Distance', 'x y dist')
    return_list = []
    distance_list = []
    # iterate over rows
    for x in grouped_comp.itertuples():
        # drop rows we already had
        for y in grouped_comp.drop(grouped_comp.index[:x.Index + 1]).itertuples():
            norm_distance = generate_dtw(x.changeMoments, y.changeMoments)
            if norm_distance < 86400:
                return_list.append((x.name, y.name))
            distance_list.append(Distance(x.name, y.name, norm_distance))

    # get highest threshold
    distance_list = sorted(distance_list, key=attrgetter('dist'))
    distance_df = pd.DataFrame(distance_list)
    distance_df.to_pickle(output_directory + "/dtw_distances.pkl")
    made_threshold = len(return_list)/len(distance_list)
    print(made_threshold)
    print("----threshold results DTW----")
    print("quartile values:")
    distances = list(map(lambda x: x.dist, distance_list))
    print_quartiles(distances)

    warpdf = pd.DataFrame(return_list, columns=['file1', 'file2'])
    return warpdf, components[['name', 'package']]


def visualise_dtw_distances(distance_list):
    ax = seaborn.violinplot(data=distance_list)
    ax.set_ylabel('distance in seconds')
    ax.set_xlabel(config.project_name)
    plt.show()


def generate_dtw(x, y):
    dynamic_warp = dtw(x=x, y=y)
    return dynamic_warp.normalizedDistance


def generate_dtw_analysis_files():
    # Create the directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    warps, changed_files = perform_dtw()

    # Add package columns
    warp_with_dates = add_info_to_cochanges(warps, changed_files)

    # 3) Store results in files
    warp_with_dates.to_csv(output_directory + "/dtw.csv")
