from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from config import input_directory

def perform_mba():
    components = pd.read_csv("input/component-characteristics-consecOnly.csv")
    # only consider classes, not packages
    orgcomponents = components[components['type'] == 'class']
    # filter on added or changed
    componentsZero = orgcomponents[orgcomponents['changeHasOccurredMetric'] == '0']
    componentsTrue = orgcomponents[orgcomponents['changeHasOccurredMetric'] == True]
    components = componentsZero.append(componentsTrue, ignore_index=True)
    length = len(components.index)
    components = components[['version', 'name']]
    # group names by version
    grouped_comp = components.groupby('version')['name'].apply(list).reset_index(name='shoppingList')
    components_list = grouped_comp['shoppingList']
    # encode list of transactions to a dataframe
    te = TransactionEncoder()
    te_ary = te.fit(components_list).transform(components_list)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # perform mba
    return generate_basket_rules(df)


def generate_basket_rules(df):
    frequent_itemsets = apriori(df, min_support=0.02, use_colnames=True, max_len=2)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)
    return rules
