from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

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
    frequent_itemsets = apriori(df, min_support=0.02, use_colnames=True, max_len=2)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)
    return rules
