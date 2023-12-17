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
    layer = Core.generate_next_layer_combinations(layer)
    while layer != set():
        logging.debug("Next layer candidates: " + str(layer))
        layer = Core.prune_itemsets(layer, data, min_support, quantity_framework)
        logging.debug("Pruned layer: " + str(layer))
        layers.append(layer)
        layer = Core.generate_next_layer_combinations(layer)

    all_layers = []
    for layer in layers:
        for itemset in layer:
            all_layers.append([itemset, Core.database_support(itemset, data)])

    columns = []
    if quantity_framework:
        columns = ['itemset', 'database_support']
    else:
        columns = ['itemset', 'transaction_support']

    print(Core.tif_hit)
    print(Core.tif_miss)


    return pd.DataFrame(all_layers, columns=columns) \
        .sort_values(columns[1], ascending=False)
