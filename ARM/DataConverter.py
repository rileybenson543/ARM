"""
    ARM - Association Rule Miner
    DataConverter - handles converting transaction
    like data into the proper format and creates
    and ARMData object
    :author Riley Basile-Benson
    :date Created: 12/16/2023
"""
import logging
import numbers

import pandas as pd
from ARM import ARMData


def convert_from_one_hot_encode(dataframe: pd.DataFrame) -> ARMData:
    transactions = []

    def create_transaction(row: pd.Series) -> ARMData:
        transaction_items = []
        items = row.items()
        for item in items:
            if isinstance(item[1], bool):
                if item[1]:
                    ti = ARMData.TransactionItem(str(item[0]), 1)
                    transaction_items.append(ti)
            elif isinstance(item[1], numbers.Number):
                if item[1] > 0:
                    ti = ARMData.TransactionItem(str(item[0]), item[1])
                    transaction_items.append(ti)
        t = ARMData.Transaction(transaction_items)
        transactions.append(t)

    dataframe.apply(create_transaction, axis=1)
    arm = ARMData.ARMData()
    arm.from_transactions(transactions)
    return arm
