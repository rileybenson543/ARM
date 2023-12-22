"""
    ARM - Association Rule Miner
    Core Functionality
    Riley Basile-Benson
    12/15/2023
"""
import itertools

import numpy as np
import time

from ARM.ARMData import *
transaction_support_cache = dict()
database_support_cache = dict()
start = 0
end = 0
times = []

def transaction_itemset_status(itemset: set, transaction: Transaction):
    if transaction.itemset.issuperset(itemset):
        return 1
    return 0



def transaction_itemset_frequency(itemset: set, transaction: Transaction):
    if transaction.itemset.issuperset(itemset):
        min = 0
        for item in transaction.items:
            if item.item in itemset:
                if item.quantity < min or min == 0:
                    min = item.quantity
        return min
    return 0


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
    f_itemset = frozenset(itemset)
    if f_itemset not in transaction_support_cache:
        t = np.zeros(len(data.columns.keys()))
        for item in itemset:
            t[data.columns[item]] = 1
        mul = np.matmul(data.matrix, t.T)
        sc = np.count_nonzero(mul == np.sum(t), axis=0)
        sup = sc / len(data)
        transaction_support_cache[f_itemset] = sup
        return sup
    else:
        return transaction_support_cache[f_itemset]



def database_support(itemset, data: ARMData):
    f_itemset = frozenset(itemset)
    if f_itemset not in database_support_cache:
        ds = database_frequency(itemset, data) / len(data)
        database_support_cache[f_itemset] = ds
        return ds
    else:
        return database_support_cache[f_itemset]


def transaction_confidence(antecedent: set, consequent: set, data):
    return transaction_support(antecedent.union(consequent), data) / transaction_support(antecedent, data)


def database_confidence(antecedent: set, consequent: set, data):
    if antecedent == set():
        return 0
    return database_support(antecedent.union(consequent), data) / database_support(antecedent, data)


def lift(antecedent: set, consequent: set, data: ARMData, quantity_framework=True):
    if quantity_framework:
        return database_confidence(antecedent, consequent, data) / database_support(consequent, data)
    else:
        return transaction_confidence(antecedent, consequent, data) / transaction_support(consequent, data)


def get_possible_items(data: ARMData):
    items = set()
    for transaction in data.transactions:
        for item in transaction.items:
            items.add(frozenset([item.item]))
    return items


def prune_itemsets(itemsets: set, data: ARMData, min_support, quantity_framework=True):
    frequent_itemsets = set()
    infrequent_itemsets = set()
    for itemset in itemsets:
        support = 0
        if quantity_framework:
            support = database_support(itemset, data)
        else:
            support = transaction_support(itemset, data)

        if support >= min_support:
            frequent_itemsets.add(itemset)
        else:
            infrequent_itemsets.add(itemset)
    if len(frequent_itemsets) == len(itemsets):
        logging.info("No itemsets were pruned. Consider increasing support")
    return frequent_itemsets, infrequent_itemsets

def prune_rules(rules: list[tuple[set, set]], data: ARMData, min_confidence, quantity_framework=True):
    if quantity_framework:
        pruned_rules = [x for x in rules if database_confidence(x[0], x[1], data) >= min_confidence]
    else:
        pruned_rules = [x for x in rules if transaction_confidence(x[0], x[1], data) >= min_confidence]

    if len(pruned_rules) == len(pruned_rules):
        logging.info("No rules were pruned. Consider increasing confidence")
    return pruned_rules



def generate_next_layer_itemset_combinations(items: set, num_items_in_combination: int, infrequent_itemsets: set):
    next_itemsets = set()
    for comb in itertools.combinations(list([x for x in items if x not in infrequent_itemsets]), num_items_in_combination):
        new_itemset = set()
        for item in comb:
            new_itemset = new_itemset.union(item)
        next_itemsets.add(frozenset(new_itemset))
    return next_itemsets


def generate_next_layer_rules_combinations(rules: list[tuple[set, set]]):
    rules_list = []
    for rule in rules:
        antecedent = list(rule[0])
        if len(antecedent) == 0:
            continue
        consequent = list(rule[1])
        consequent.append(antecedent[-1])
        rules_list.append((set(antecedent[:-1]), set(consequent)))
    return rules_list