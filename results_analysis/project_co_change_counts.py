import numpy as np

from results_analysis.results_analysis_helper import get_analysis_results
import matplotlib.pyplot as plt


# Shows the amount of co-change pairs for the three approaches per project.
# Done on a log-scale to see the difference amongst algorithms.
def algorithm_cc_count_comparison():
    result_df = get_analysis_results()
    ax = result_df[['DTW_cc_pairs', 'MBA_cc_pairs', 'FO_cc_pairs']].plot(kind='bar', title="Co-change pairs per algorithm grouped by project", figsize=(15, 10), legend=True, fontsize=12, logy=True)
    ax.set_xlabel("Project", fontsize=12)
    ax.set_ylabel("Co-changing pairs", fontsize=12)
    ax.set_xticklabels(result_df.project)
    plt.show()


# Shows how many co-change pairs each project has.
def project_cc_count_comparison():
    result_df = get_analysis_results()
    ax = result_df[['DTW_cc_pairs', 'MBA_cc_pairs', 'FO_cc_pairs']].plot(kind='bar', title="Co-change pairs per algorithm grouped by project", figsize=(15, 10), legend=True, fontsize=12)
    ax.set_xlabel("Project", fontsize=12)
    ax.set_ylabel("Co-changing pairs", fontsize=12)
    ax.set_xticklabels(result_df.project)
    plt.show()

