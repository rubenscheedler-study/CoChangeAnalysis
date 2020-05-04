from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
import numpy as np

from helper_scripts.components_helper import get_components


def perform_mba():
    components = get_components()
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
    return rules, components['name']


def generate_basket_rules(df):
    all_itemsets = apriori(df, min_support=0.0000001, use_colnames=True, max_len=2)
    distance_list = sorted(all_itemsets['support'])
    print("----threshold results mba support----")
    print("quartile values:")
    firstquartile = np.percentile(distance_list, 25)
    median = np.percentile(distance_list, 50)
    thirdquartile = np.percentile(distance_list, 75)
    print("90% at threshold: ", np.percentile(distance_list, 90))
    print("95% at threshold: ", np.percentile(distance_list, 95))
    print(firstquartile, median, thirdquartile)


    rules = association_rules(all_itemsets, metric="confidence", min_threshold=0.0)
    distance_list = sorted(rules['confidence'])
    print("----threshold results mba confidence without support threshold----")
    print("quartile values:")
    firstquartile = np.percentile(distance_list, 25)
    median = np.percentile(distance_list, 50)
    thirdquartile = np.percentile(distance_list, 75)
    print("90% at threshold: ", np.percentile(distance_list, 90))
    print("95% at threshold: ", np.percentile(distance_list, 95))
    print(firstquartile, median, thirdquartile)



    frequent_itemsets = apriori(df, min_support=0.02, use_colnames=True, max_len=2)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.0)
    distance_list = sorted(rules['confidence'])
    print("----threshold results mba confidence after support threshold----")
    print("quartile values:")
    firstquartile = np.percentile(distance_list, 25)
    median = np.percentile(distance_list, 50)
    thirdquartile = np.percentile(distance_list, 75)
    print("90% at threshold: ", np.percentile(distance_list, 90))
    print("95% at threshold: ", np.percentile(distance_list, 95))
    print(firstquartile, median, thirdquartile)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)
    return rules
