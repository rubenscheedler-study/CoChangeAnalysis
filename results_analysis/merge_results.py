import pandas as pd

from results_analysis.results_analysis_helper import get_analysis_results


def merge_results(merge=True, include_meta_data=True):
    result_df = pd.read_csv('../analysis_results_rq3.csv')

    if merge:
        extra_results = pd.read_csv('../analysis_results_class_ronald.csv')
        result_df = result_df.append(extra_results)

    # Add project metadata
    if include_meta_data:
        result_df = add_meta_data(result_df)

    # Persist to file
    result_df.to_csv('../analysis_results_merged.csv', index=False)


def add_meta_data(result_df):
    meta_data_df = pd.read_csv('../meta_data.csv')
    meta_data_df = meta_data_df[['project', 'analysis_end_date', 'analysis_start_date', 'commits_analyzed', 'threshold', 'domain']]
    meta_data_df = meta_data_df.rename(columns={'project': 'project2'})

    result_meta_df = result_df.merge(meta_data_df, how='inner', left_on=['project'], right_on=['project2'])
    result_meta_df = result_meta_df.drop(columns=['project2'], axis=1)
    return result_meta_df


merge_results(False, True)
