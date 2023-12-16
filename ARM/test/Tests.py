import unittest

import pandas as pd

from ARM import Core, ItemsetGenerator, ARMData

data_list = [
        [('a', 1), ('b', 1)],
        [('a', 2), ('b', 3), ('c', 2)],
        [('a', 1), ('b', 4), ('e', 1)],
        [('a', 3), ('e', 1)],
        [('c', 2), ('f', 2)]
    ]
data = ARMData.ARMData()
data.from_list(data_list)


class ItemsetTests(unittest.TestCase):
    def test_transaction_support(self):
        self.assertEqual(0.6, Core.transaction_support({'a', 'b'}, data))

    def test_database_support(self):
        self.assertEqual(0.8, Core.database_support({'a', 'b'}, data))

    def test_transaction_itemset_status_case1(self):
        transaction = data.transactions[1]
        itemset = {'a', 'b'}
        tis = Core.transaction_itemset_status(itemset, transaction)
        self.assertEqual(1, tis)

    def test_transaction_itemset_status_case2(self):
        transaction = data.transactions[4]
        itemset = {'a', 'b'}
        tis = Core.transaction_itemset_status(itemset, transaction)
        self.assertEqual(0, tis)

    def test_transaction_itemset_frequency_case1(self):
        transaction = data.transactions[2]
        itemset = {'a', 'b'}
        tif = Core.transaction_itemset_frequency(itemset, transaction)
        self.assertEqual(1, tif)

    def test_transaction_itemset_frequency_case2(self):
        transaction = data.transactions[4]
        itemset = {'a', 'b'}
        tif = Core.transaction_itemset_frequency(itemset, transaction)
        self.assertEqual(0, tif)

    def test_transaction_frequency_case1(self):
        itemset = {'a', 'b'}
        tf = Core.transaction_frequency(itemset, data)
        self.assertEqual(3, tf)

    def test_database_frequency_case1(self):
        itemset = {'a', 'b'}
        df = Core.database_frequency(itemset, data)
        self.assertEqual(4, df)

    def test_database_frequency_case2(self):
        itemset = {'a'}
        df = Core.database_frequency(itemset, data)
        self.assertEqual(7, df)


class RuleTests(unittest.TestCase):
    def test_transaction_confidence_case1(self):
        # rule: a -> b
        antecedent = {'a'}
        consequent = {'b'}
        tc = Core.transaction_confidence(antecedent, consequent, data)
        self.assertEqual(0.75, round(tc, 2))

    def test_transaction_confidence_case2(self):
        # rule: a -> f
        antecedent = {'a'}
        consequent = {'f'}
        tc = Core.transaction_confidence(antecedent, consequent, data)
        self.assertEqual(0, tc)

    def test_transaction_confidence_case3(self):
        # rule: b -> c
        antecedent = {'b'}
        consequent = {'c'}
        tc = Core.transaction_confidence(antecedent, consequent, data)
        self.assertEqual(0.33, round(tc, 2))

    def test_database_confidence_case1(self):
        # rule: b -> c
        antecedent = {'a'}
        consequent = {'b'}
        dc = Core.database_confidence(antecedent, consequent, data)
        self.assertEqual(0.57, round(dc, 2))

    def test_database_confidence_case2(self):
        # rule: a -> f
        antecedent = {'a'}
        consequent = {'f'}
        dc = Core.database_confidence(antecedent, consequent, data)
        self.assertEqual(0, dc)

    def test_database_confidence_case3(self):
        # rule: b -> c
        antecedent = {'b'}
        consequent = {'c'}
        dc = Core.database_confidence(antecedent, consequent, data)
        self.assertEqual(0.25, round(dc, 2))

    def test_get_possible_items_case1(self):
        possible_items = Core.get_possible_items(data)
        self.assertEqual({'a', 'b', 'c', 'e', 'f'}, possible_items)

    def test_get_possible_items_case2(self):
        data1 = ARMData.ARMData()  # empty data
        possible_items = Core.get_possible_items(data1)
        self.assertEqual(set(), possible_items)

    def test_prune_itemsets_case1_no_quantity(self):
        min_support = 0.5
        pruned = Core.prune_itemsets({'a', 'b', 'c', 'e', 'f'}, data, min_support, quantity_framework=False)
        self.assertEqual({'a', 'b'}, pruned)

    def test_prune_itemsets_case2_with_quantity(self):
        min_support = 0.5
        pruned = Core.prune_itemsets({'a', 'b', 'c', 'e', 'f'}, data, min_support, quantity_framework=True)
        self.assertEqual({'a', 'b', 'c'}, pruned)

    def test_prune_itemset_case3_no_quantity(self):
        min_support = 0.0
        pruned = Core.prune_itemsets({'a', 'b', 'c', 'e', 'f'}, data, min_support, quantity_framework=False)
        self.assertEqual({'a', 'b', 'c', 'e', 'f'}, pruned)

    def test_prune_itemset_case4_with_quantity(self):
        min_support = 0.0
        pruned = Core.prune_itemsets({'a', 'b', 'c', 'e', 'f'}, data, min_support, quantity_framework=True)
        self.assertEqual({'a', 'b', 'c', 'e', 'f'}, pruned)

    def test_generate_next_layer_combinations_case1(self):
        itemsets = {'a', 'b', 'c'}
        next_layer = Core.generate_next_layer_combinations(itemsets)
        self.assertEqual({frozenset({'a', 'c'}), frozenset({'b', 'c'}), frozenset({'a', 'b'})}, next_layer)

    def test_generate_next_layer_combinations_case2(self):
        itemsets = {'a'}
        next_layer = Core.generate_next_layer_combinations(itemsets)
        self.assertEqual(set(), next_layer)

    def test_generate_next_layer_combinations_case3(self):
        itemsets = {'a', 'b', 'c', 'd', 'e'}
        next_layer = Core.generate_next_layer_combinations(itemsets)
        self.assertEqual({frozenset({'b', 'e'}), frozenset({'b', 'd'}), frozenset({'a', 'd'}),
                          frozenset({'c', 'e'}), frozenset({'a', 'b'}), frozenset({'b', 'c'}),
                          frozenset({'a', 'c'}), frozenset({'d', 'e'}), frozenset({'c', 'd'}),
                          frozenset({'a', 'e'})}, next_layer)


if __name__ == '__main__':
    unittest.main()
