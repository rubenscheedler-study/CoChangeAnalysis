import os

import seaborn
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
import numpy as np
import matplotlib.pyplot as plt

from config import output_directory
from helper_scripts.changes_helper import get_changes
from helper_scripts.file_pair_helper import add_info_to_cochanges


def perform_mba():
    components = get_changes()
    # group names by version
    grouped_comp = components.groupby('version')['name'].apply(list).reset_index(name='shoppingList')
    components_list = grouped_comp['shoppingList']
    # encode list of transactions to a dataframe
    te = TransactionEncoder()
    te_ary = te.fit(components_list).transform(components_list)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # perform mba
    rules = generate_basket_rules(df)
    rules['file1'] = list(map(lambda x: next(iter(x)), rules['antecedents']))
    rules['file2'] = list(map(lambda x: next(iter(x)), rules['consequents']))
    return rules, components[['name', 'package']]


def generate_basket_rules(df):
    all_itemsets = apriori(df, min_support=0.0000001, use_colnames=True, max_len=2)
    all_itemsets.to_pickle(output_directory + "/mba_support_0.pkl")
    supp0 = sorted(all_itemsets['support'])
    print("----threshold results mba support----")
    print_quartiles(supp0)

    rules = association_rules(all_itemsets, metric="confidence", min_threshold=0.0)
    rules.to_pickle(output_directory + "/mba_conf_0_supp_0.pkl")
    conf_0_supp0 = sorted(rules['confidence'])
    print("----threshold results mba confidence without support threshold----")
    print_quartiles(conf_0_supp0)

    frequent_itemsets = apriori(df, min_support=0.02, use_colnames=True, max_len=2)
    frequent_itemsets.to_pickle(output_directory + "/mba_support_2.pkl")
    supp2 = sorted(frequent_itemsets['support'])

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.0)
    rules.to_pickle(output_directory + "/mba_conf_0_supp_2.pkl")

    conf_0_supp2 = sorted(rules['confidence'])

    #TODO: extract to proper function
    #seaborn.violinplot(data=supp0)
    #plt.show()
    #seaborn.violinplot(data=conf_0_supp0)
    #plt.show()
    #seaborn.violinplot(data=supp2)
    #plt.show()
    #seaborn.violinplot(data=conf_0_supp2)
    #plt.show()

    print("----threshold results mba confidence after support threshold----")
    if len(conf_0_supp2) == 0:
        print("Quartiles could not be calculated. conf_0_supp2 is empty.")
    else:
        print_quartiles(conf_0_supp2)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)
    rules.to_pickle(output_directory + "/mba_conf_8.pkl")
    return rules


def print_quartiles(arr):
    print("quartile values:")
    first_quartile = np.percentile(arr, 25)
    median = np.percentile(arr, 50)
    third_quartile = np.percentile(arr, 75)
    print("90% at threshold: ", np.percentile(arr, 90))
    print("95% at threshold: ", np.percentile(arr, 95))
    print(first_quartile, median, third_quartile)


def generate_mba_analysis_files():
    # Create the directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    rules, changed_files = perform_mba()

    # 1) Build the dataframe containing the co-changes
    rules_with_dates = add_info_to_cochanges(rules, changed_files)

    rules_with_dates.to_csv(output_directory + "/mba.csv")


