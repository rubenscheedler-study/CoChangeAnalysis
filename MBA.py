from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

def perform_mba():
    components = pd.read_csv("input/component-characteristics-consecOnly.csv")
    components = components[components['type'] == 'class']
    components = components[components.apply(lambda row: row['changeHasOccurredMetric'] == '0' or row['changeHasOccurredMetric'] == 'True', axis=1)]
    components = components[['version', 'name']]
    grouped_comp = components.groupby('version')['name'].apply(list).reset_index(name='shoppingList')
    components_list = grouped_comp['shoppingList']
    te = TransactionEncoder()
    te_ary = te.fit(components_list).transform(components_list)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    x = generate_basket_rules(df)
    y= 5



def generate_basket_rules(df):
    frequent_itemsets = apriori(df, min_support=0.02, use_colnames=True, max_len=2)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)
    return rules
