import os
from collections import namedtuple
from operator import attrgetter

import seaborn
from dtw import dtw
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import config
from Utility import get_class_from_package
from config import output_directory
from helper_scripts.Commit_date_helper import convert_hashlist_to_datelist, add_file_dates
from helper_scripts.components_helper import get_components
from helper_scripts.file_pair_helper import filter_duplicate_file_pairs, generate_all_pairs


def perform_dtw():
    components = get_components()
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
            normDistance = generate_dtw(x.changeMoments, y.changeMoments)
            if normDistance < 86400:
                return_list.append((x.name, y.name))
            distance_list.append(Distance(x.name, y.name, normDistance))

    # get highest threshold
    distance_list = sorted(distance_list, key=attrgetter('dist'))
    distance_df = pd.DataFrame(distance_list)
    distance_df.to_pickle(output_directory + "/dtw_distances.pkl")
    made_threshold = len(return_list)/len(distance_list)
    print(made_threshold)
    print("----threshold results DTW----")
    print("quartile values:")
    distances = list(map(lambda x: x.dist, distance_list))
    visualise_dtw_distances(distances)
    firstquartile = np.percentile(distances, 25)
    median = np.percentile(distances, 50)
    thirdquartile = np.percentile(distances, 75)
    print("10% at threshold: ", np.percentile(distances, 10))
    print("1% at threshold: ", np.percentile(distances, 1))
    print(firstquartile, median, thirdquartile)


    warpdf = pd.DataFrame(return_list, columns=['file1', 'file2'])
    return warpdf, components['name']


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

    # 1) Build the dataframe containing the co-changes
    warpdf = filter_duplicate_file_pairs(warps) # df: file1, file2
    # Add package columns
    warpdf['package1'] = warpdf["file1"].str.rsplit(".", 1).str[0]
    warpdf['package2'] = warpdf["file2"].str.rsplit(".", 1).str[0]
    warp_with_dates = add_file_dates(warpdf)
    # Map files to class.java
    warp_with_dates['file1'] = warp_with_dates['file1'].apply(get_class_from_package)
    warp_with_dates['file2'] = warp_with_dates['file2'].apply(get_class_from_package)

    # 2) Build the dataframe containing all changed pairs
    all_pairs = generate_all_pairs(changed_files)  # df: file1, file2
    all_pairs['package1'] = all_pairs["file1"].str.rsplit(".", 1).str[0]
    all_pairs['package2'] = all_pairs["file2"].str.rsplit(".", 1).str[0]
    # Map files to class.java
    all_pairs['file1'] = all_pairs['file1'].apply(get_class_from_package)
    all_pairs['file2'] = all_pairs['file2'].apply(get_class_from_package)

    # 3) Store results in files
    warp_with_dates.to_csv(output_directory + "/dtw.csv")
    all_pairs.to_csv(output_directory + "/file_pairs_dtw.csv")
