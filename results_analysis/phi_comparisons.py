import pandas as pd

from results_analysis.results_analysis_helper import get_analysis_results
import matplotlib.pyplot as plt


# Shows a scatter plot of phi values vs the analysed time-range they apply to.
def phi_vs_time_range():
    result_df = get_analysis_results()
    result_df['analysis_range'] = [x.days for x in result_df.analysis_end_date - result_df.analysis_start_date]

    ax1 = result_df.plot(kind='scatter', x='analysis_range', y='DTW_chi_phi', color='blue', title="Phi-values set out against project analysis interval", legend=True)
    ax2 = result_df.plot(kind='scatter', x='analysis_range', y='MBA_chi_phi', color='green', ax=ax1)
    ax3 = result_df.plot(kind='scatter', x='analysis_range', y='FO_chi_phi', color='orange', ax=ax1)
    ax1.set_xlabel("Length of analysis time interval", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)
    plt.show()


# Shows a scatter plot of phi values vs the total amount of file pairs (~ project size).
def phi_vs_all_pairs():
    result_df = get_analysis_results()

    ax1 = result_df.plot(kind='scatter', x='DTW_all_pairs', y='DTW_chi_phi', color='blue', title="Phi-values set out against project size", legend=True)
    ax2 = result_df.plot(kind='scatter', x='MBA_all_pairs', y='MBA_chi_phi', color='green', ax=ax1)
    ax3 = result_df.plot(kind='scatter', x='FO_all_pairs', y='FO_chi_phi', color='orange', ax=ax1)
    ax1.set_xlabel("Amount of changed file pairs", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)
    plt.show()