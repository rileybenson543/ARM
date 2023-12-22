"""
    ARM - Association Rule Miner
    ARMData class
    Riley Basile-Benson
    12/16/2023
"""
import logging
from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class TransactionItem:
    item: str
    quantity: int

    def __init__(self, item: str, quantity: int):
        self.item = item
        self.quantity = quantity


@dataclass
class Transaction:

    items: list[TransactionItem]
    itemset: frozenset

    def __init__(self, items: list[TransactionItem]):
        self.items = items
        self.itemset = frozenset([x.item for x in items])


class ARMData:

    transactions: list[Transaction] = []
    num_transactions: int = 0
    matrix: np.ndarray
    columns: dict[str, int] = {}

    def __init__(self):
        self.transactions = []
        self.num_transactions = 0

    def from_transactions(self, data: list[Transaction]):
        self.transactions = data
        self.num_transactions = len(data)
        self.generate_matrix()
        pass

    def from_list(self, data: list[list[tuple[str, int]]]):
        for transaction in data:
            transaction_list = []
            for item_record in transaction:
                transaction_list.append(TransactionItem(item_record[0], item_record[1]))
            t = Transaction(transaction_list)
            self.transactions.append(t)

        self.num_transactions = len(self.transactions)
        self.generate_matrix()

    def generate_column_index_definitions(self):
        col_idx = 0
        for idx, transaction in enumerate(self.transactions):
            for item in transaction.items:
                if item.item not in self.columns:
                    self.columns[item.item] = col_idx
                    col_idx += 1

    def generate_matrix(self):
        if len(self.columns.keys()) == 0:
            self.generate_column_index_definitions()

        data = []
        for transaction in self.transactions:
            transaction_arr = np.zeros(len(self.columns.keys()))
            for item in transaction.items:
                transaction_arr[self.columns[item.item]] = 1
            data.append(transaction_arr)

        self.matrix = np.asarray(data)

    def __len__(self):
        return self.num_transactions

    def __str__(self):
        string = ""
        for transaction in self.transactions:
            string += str(transaction) + "\n"
        return string
