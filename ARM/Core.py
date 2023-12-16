"""
    ARM - Association Rule Miner
    Core Functionality
    Riley Basile-Benson
    12/15/2023
"""

from ARM.ARMData import *


def transaction_itemset_status(itemset, transaction: Transaction):
    to_find = set(itemset)
    for item in transaction.items:
        if item.item in itemset:
            to_find.remove(item.item)
    if len(to_find) == 0:
        return 1
    return 0


def transaction_itemset_frequency(itemset: set, transaction: Transaction):
    found = []
    min = 0
    for item in transaction.items:
        if item.item in itemset:
            found.append(item.item)
            if item.quantity < min or min == 0:
                min = item.quantity

    for item in itemset:
        if item not in found:
            return 0

    return min


def transaction_frequency(itemset, data: ARMData):
    total = 0
    for transaction in data.transactions:
        total += transaction_itemset_status(itemset, transaction)
    return total


def database_frequency(itemset, data: ARMData):
    total = 0
    for transaction in data.transactions:
        total += transaction_itemset_frequency(itemset, transaction)
    return total


def transaction_support(itemset, data: ARMData):
    return transaction_frequency(itemset, data) / len(data)


def database_support(itemset, data: ARMData):
    return database_frequency(itemset, data) / len(data)


def transaction_confidence(antecedent: set, consequent: set, data):
    return transaction_support(antecedent.union(consequent), data) / transaction_support(antecedent, data)


def database_confidence(antecedent: set, consequent: set, data):
    return database_support(antecedent.union(consequent), data) / database_support(antecedent, data)


def get_possible_items(data: ARMData):
    items = set()
    for transaction in data.transactions:
        for item in transaction.items:
            items.add(item.item)
    return items


def prune_itemsets(itemsets: set, data, min_support=0.1, quantity_framework=True):
    pruned_itemsets = set()
    for itemset in itemsets:

        support = 0
        if quantity_framework:
            support = database_support(itemset, data)
        else:
            support = transaction_support(itemset, data)

        if support >= min_support:
            pruned_itemsets.add(itemset)
    return pruned_itemsets


def generate_next_layer_combinations(itemsets: set):
    itemsets_list = list(itemsets)
    combinations = set()
    for idx in range(len(itemsets_list)-1):
        for next in range(idx+1, len(itemsets_list)):
            combinations.add(frozenset(set(itemsets_list[idx]).union(set(itemsets_list[next]))))
    return combinations
