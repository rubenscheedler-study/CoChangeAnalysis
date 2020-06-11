import pandas as pd

from results_analysis.results_analysis_helper import get_analysis_results


def merge_results():
    result_df = pd.read_csv('../analysis_results.csv')
    extra_results = pd.read_csv('../analysis_results_poi.csv')
    result_df = result_df.append(extra_results)
    result_df.to_csv('../analysis_results_merged.csv', index=False)


merge_results()
