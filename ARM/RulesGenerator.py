"""
    ARM - Association Rule Miner
    Rules Generator - generates rules given
        a list of frequent itemsets
    Riley Basile-Benson
    12/17/2023
"""
import pandas as pd
import logging
from ARM import Core
import ARM

def generate_rules(itemsets: pd.DataFrame, data: ARM.ARMData, min_confidence, quantity_framework=True):
    if len(itemsets.columns) > 2:
        logging.error("Itemset Dataframe should not contain more than 2 columns.")
        return None
    if itemsets.columns[0] != 'itemset' or itemsets.columns[1].split('_')[1] != 'support':
        logging.error("Itemset Dataframe contains invalid columns")
        return None

    layers = []
    layer = [(x, set()) for x in itemsets['itemset']]
    while len(layer) > 0:
        layer = ARM.Core.generate_next_layer_rules_combinations(layer)
        logging.info("Pruning layer")
        layer = ARM.Core.prune_rules(layer, data, min_confidence, quantity_framework)
        layers.append(layer)

    all_layers = []
    for layer in layers:
        for rule in layer:
            confidence = 0
            if quantity_framework:
                confidence = Core.database_confidence(rule[0], rule[1], data)
            else:
                confidence = Core.transaction_confidence(rule[0], rule[1], data)
            all_layers.append([rule, confidence,
                               Core.lift(rule[0], rule[1], data, quantity_framework)])

    df = pd.DataFrame(all_layers, columns=['rule', 'confidence', 'lift']).sort_values('lift', ascending=False)

    return df
