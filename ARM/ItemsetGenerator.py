"""
    ARM - Association Rule Miner
    Itemset Generator
    Riley Basile-Benson
    12/16/2023
"""

from ARM import Core
import pandas as pd
import logging


def generate_itemsets(data, min_support, quantity_framework=True):
    layers = []
    layer = Core.prune_itemsets(Core.get_possible_items(data), data, min_support, quantity_framework)
    while Core.generate_next_layer_combinations(layer) != set():
        next_layer = Core.generate_next_layer_combinations(layer)
        logging.debug("Next layer candidates: " + str(next_layer))
        layer = Core.prune_itemsets(next_layer, data, min_support, quantity_framework)
        logging.debug("Pruned layer: " + str(layer))
        layers.append(layer)

    all_layers = []
    for layer in layers:
        for itemset in layer:
            all_layers.append([itemset, Core.database_support(itemset, data)])

    columns = []
    if quantity_framework:
        columns = ['itemset', 'database_support']
    else:
        columns = ['itemset', 'transaction_support']

    return pd.DataFrame(all_layers, columns=columns) \
        .sort_values(columns[1], ascending=False)
