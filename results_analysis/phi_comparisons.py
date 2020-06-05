import pandas as pd

from results_analysis.results_analysis_helper import get_analysis_results, label_points
import matplotlib.pyplot as plt


# Shows a scatter plot of phi values vs the analysed time-range they apply to.
def phi_vs_time_range():
    result_df = get_analysis_results()
    result_df['analysis_range'] = [x.days for x in result_df.analysis_end_date - result_df.analysis_start_date]

    '''domains = result_df.Domain.unique()

    for domain in domains:
        domain_rows = result_df[result_df.Domain == domain]
        ax1 = domain_rows.plot(kind='scatter', x='analysis_range', y='DTW_chi_phi', color='blue',
                             title="Phi-values set out against project analysis interval for domain " + domain, legend=True)
        ax2 = domain_rows.plot(kind='scatter', x='analysis_range', y='MBA_chi_phi', color='green', ax=ax1)
        ax3 = domain_rows.plot(kind='scatter', x='analysis_range', y='FO_chi_phi', color='orange', ax=ax1)
        ax1.set_xlabel("Length of analysis time interval", fontsize=12)
        ax1.set_ylabel("Phi-value", fontsize=12)

        label_points(domain_rows.analysis_range, domain_rows.DTW_chi_phi, domain_rows.project, ax1)
        label_points(domain_rows.analysis_range, domain_rows.MBA_chi_phi, domain_rows.project, ax1)
        label_points(domain_rows.analysis_range, domain_rows.FO_chi_phi, domain_rows.project, ax1)
        plt.show()
    commitSizeMean = result_df.commits_analyzed.mean()
    sub_threshold = result_df[result_df.commits_analyzed < commitSizeMean]
    ax1 = sub_threshold.plot(kind='scatter', x='analysis_range', y='DTW_chi_phi', color='blue',
                           title="Phi-values set out against project analysis interval for below mean",
                           legend=True)
    ax2 = sub_threshold.plot(kind='scatter', x='analysis_range', y='MBA_chi_phi', color='green', ax=ax1)
    ax3 = sub_threshold.plot(kind='scatter', x='analysis_range', y='FO_chi_phi', color='orange', ax=ax1)
    ax1.set_xlabel("Length of analysis time interval", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)

    label_points(sub_threshold.analysis_range, sub_threshold.DTW_chi_phi, sub_threshold.project, ax1)
    label_points(sub_threshold.analysis_range, sub_threshold.MBA_chi_phi, sub_threshold.project, ax1)
    label_points(sub_threshold.analysis_range, sub_threshold.FO_chi_phi, sub_threshold.project, ax1)
    plt.show()


    super_threshold = result_df[result_df.commits_analyzed >= commitSizeMean]
    ax1 = super_threshold.plot(kind='scatter', x='analysis_range', y='DTW_chi_phi', color='blue',
                           title="Phi-values set out against project analysis interval above mean",
                           legend=True)
    ax2 = super_threshold.plot(kind='scatter', x='analysis_range', y='MBA_chi_phi', color='green', ax=ax1)
    ax3 = super_threshold.plot(kind='scatter', x='analysis_range', y='FO_chi_phi', color='orange', ax=ax1)
    ax1.set_xlabel("Length of analysis time interval", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)

    label_points(super_threshold.analysis_range, super_threshold.DTW_chi_phi, super_threshold.project, ax1)
    label_points(super_threshold.analysis_range, super_threshold.MBA_chi_phi, super_threshold.project, ax1)
    label_points(super_threshold.analysis_range, super_threshold.FO_chi_phi, super_threshold.project, ax1)
    plt.show()

    '''

    ax1 = result_df.plot(kind='scatter', x='analysis_range', y='DTW_chi_phi', color='blue', title="Phi-values set out against project analysis interval for all projects", legend=True)
    ax2 = result_df.plot(kind='scatter', x='analysis_range', y='MBA_chi_phi', color='green', ax=ax1)
    ax3 = result_df.plot(kind='scatter', x='analysis_range', y='FO_chi_phi', color='orange', ax=ax1)
    ax1.set_xlabel("Length of analysis time interval", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)

    label_points(result_df.analysis_range, result_df.DTW_chi_phi, result_df.project, ax1)
    label_points(result_df.analysis_range, result_df.MBA_chi_phi, result_df.project, ax1)
    label_points(result_df.analysis_range, result_df.FO_chi_phi, result_df.project, ax1)

    plt.show()


# Shows a scatter plot of phi values vs the total amount of file pairs (~ project size).
def phi_vs_all_pairs():
    result_df = get_analysis_results()

    ax1 = result_df.plot(kind='scatter', x='DTW_all_pairs', y='DTW_chi_phi', color='blue', title="Phi-values set out against project size", legend=True)
    ax2 = result_df.plot(kind='scatter', x='MBA_all_pairs', y='MBA_chi_phi', color='green', ax=ax1, legend=True)
    ax3 = result_df.plot(kind='scatter', x='FO_all_pairs', y='FO_chi_phi', color='orange', ax=ax1, legend=True)
    ax1.set_xlabel("Amount of changed file pairs", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)

    label_points(result_df.DTW_all_pairs, result_df.DTW_chi_phi, result_df.project, ax1)
    label_points(result_df.MBA_all_pairs, result_df.MBA_chi_phi, result_df.project, ax1)
    label_points(result_df.FO_all_pairs, result_df.FO_chi_phi, result_df.project, ax1)

    plt.show()


# Compares the phi value against the amount of commits analyzed by arcan
def phi_vs_commits_analyzed():
    result_df = get_analysis_results()

    ax1 = result_df.plot(kind='scatter', x='commits_analyzed', y='DTW_chi_phi', color='blue', title="Phi value set out against commits analyzed", legend=True)
    ax2 = result_df.plot(kind='scatter', x='commits_analyzed', y='MBA_chi_phi', color='green', ax=ax1, legend=True)
    ax3 = result_df.plot(kind='scatter', x='commits_analyzed', y='FO_chi_phi', color='orange', ax=ax1, legend=True)
    ax1.set_xlabel("Commits analyzed", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)

    label_points(result_df.commits_analyzed, result_df.DTW_chi_phi, result_df.project, ax1)
    label_points(result_df.commits_analyzed, result_df.MBA_chi_phi, result_df.project, ax1)
    label_points(result_df.commits_analyzed, result_df.FO_chi_phi, result_df.project, ax1)

    plt.show()


# Compares the phi value against the match threshold used while filtering co-changes.
def phi_vs_threshold():
    result_df = get_analysis_results()

    ax1 = result_df.plot(kind='scatter', x='threshold', y='FO_chi_phi', color='blue', title="Phi value set out against the match threshold applied during FO analysis", legend=True)
    ax1.set_xlabel("Threshold", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)

    label_points(result_df.threshold, result_df.FO_chi_phi, result_df.project, ax1)

    plt.show()


# Compares the phi value against the percentage of file pairs marked as co-changing
def phi_vs_cc_ratio():
    result_df = get_analysis_results()
    result_df['DTW_cc_ratio'] = [100 * x for x in result_df.DTW_cc_pairs / result_df.DTW_all_pairs]
    result_df['MBA_cc_ratio'] = [100 * x for x in result_df.MBA_cc_pairs / result_df.MBA_all_pairs]
    result_df['FO_cc_ratio'] = [100 * x for x in result_df.FO_cc_pairs / result_df.FO_all_pairs]

    ax1 = result_df.plot(kind='scatter', x='DTW_cc_ratio', y='DTW_chi_phi', color='blue', title="Phi-values set out against co-change ratio", legend=True)
    ax2 = result_df.plot(kind='scatter', x='MBA_cc_ratio', y='MBA_chi_phi', color='green', ax=ax1)
    ax3 = result_df.plot(kind='scatter', x='FO_cc_ratio', y='FO_chi_phi', color='orange', ax=ax1)
    ax1.set_xlabel("Percentage of file pairs marked as co-change", fontsize=12)
    ax1.set_ylabel("Phi-value", fontsize=12)

    label_points(result_df.DTW_cc_ratio, result_df.DTW_chi_phi, result_df.project, ax1)
    label_points(result_df.MBA_cc_ratio, result_df.MBA_chi_phi, result_df.project, ax1)
    label_points(result_df.FO_cc_ratio, result_df.FO_chi_phi, result_df.project, ax1)

    plt.show()