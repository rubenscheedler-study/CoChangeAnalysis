from results_analysis.phi_comparisons import phi_vs_time_range, phi_vs_all_pairs
from results_analysis.project_co_change_counts import algorithm_cc_count_comparison, project_cc_count_comparison


def result_analysis():
    algorithm_cc_count_comparison()
    project_cc_count_comparison()
    phi_vs_time_range()
    phi_vs_all_pairs()
