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
    layer_num = 1
    possible_items = Core.get_possible_items(data)
    logging.info(f"Staring with with {len(possible_items)} itemsets at layer {layer_num}")
    layer, infrequent_itemsets = Core.prune_itemsets(possible_items, data, min_support, quantity_framework)
    layer = Core.generate_next_layer_itemset_combinations(possible_items, layer_num + 1, infrequent_itemsets)
    logging.info(f"Generated {len(layer)} candidate itemsets")
    while len(layer) > 0:
        layer_num += 1
        logging.debug("Next layer candidates: " + str(layer))
        layer, infrequent = Core.prune_itemsets(layer, data, min_support, quantity_framework)
        logging.info(f"Pruned {len(infrequent)} itemsets")
        infrequent_itemsets.union(infrequent)
        logging.debug("Pruned layer: " + str(layer))
        layers.append(layer)
        layer = Core.generate_next_layer_itemset_combinations(possible_items, layer_num + 1, infrequent_itemsets)
        logging.info(f"Generated {len(layer)} candidate itemsets")

    all_layers = []
    for layer in layers:
        for itemset in layer:
            support = 0
            if quantity_framework:
                support = Core.database_support(itemset, data)
            else:
                support = Core.transaction_support(itemset, data)
            all_layers.append([itemset, support])

    columns = []
    if quantity_framework:
        columns = ['itemset', 'database_support']
    else:
        columns = ['itemset', 'transaction_support']

    return pd.DataFrame(all_layers, columns=columns) \
        .sort_values(columns[1], ascending=False)
