import logging

import ARM
from ARM import ARMData

data = [
        [('a', 1), ('b', 1)],
        [('a', 2), ('b', 3), ('c', 2)],
        [('a', 1), ('b', 4), ('e', 1)],
        [('a', 3), ('e', 1)],
        [('c', 2), ('f', 2)]
]

arm_data = ARM.ARMData.ARMData()
arm_data.from_list(data)
df = ARM.ItemsetGenerator.generate_itemsets(arm_data, 0.4, quantity_framework=True)
print(df)
df = ARM.ItemsetGenerator.generate_itemsets(arm_data, 0.4, quantity_framework=False)
print(df)
