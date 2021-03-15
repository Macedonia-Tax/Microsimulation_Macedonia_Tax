# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:04:25 2020

@author: WB544155
"""

import pandas as pd
import numpy as np


sample_data = pd.read_csv("taxcalc/pit_macedonia.csv")

unique_taxpayers = 786682
sample_per_decile = 10000
taxpayers_per_decile = unique_taxpayers/10
weight = taxpayers_per_decile/sample_per_decile

"""
m = sample_data.deciles
n = np.where(m = 1,2,3,4,7,8,9,10)
l = np.where(m = 5,6)


if sample_data.deciles == (1 or 2 or 3 or 4 or 7 or 8 or 9 or 10):
    sample_per_decile = 10000
else:
    sample_per_decile = 10001
       
np.where(sample_per_decile = 10000(np.where(sample_per_decile = 10001)))

sample_per_decile1 = 10000
sample_per_decile2 = 10001
weights1 = taxpayers_per_decile/sample_per_decile1
weights2 = weight1 = taxpayers_per_decile/sample_per_decile2
"""

data = np.zeros(len(sample_data))
weights_df = pd.DataFrame(data, columns=['WT2019'])
weights_df['WT2019'] = weight

growth_rate_tax_filers = 0
weights_df['WT2020'] = weights_df['WT2019'] * (1+growth_rate_tax_filers)
weights_df['WT2021'] = weights_df['WT2020'] * (1+growth_rate_tax_filers)
weights_df['WT2022'] = weights_df['WT2021'] * (1+growth_rate_tax_filers)
weights_df['WT2023'] = weights_df['WT2022'] * (1+growth_rate_tax_filers)
weights_df['WT2024'] = weights_df['WT2023'] * (1+growth_rate_tax_filers)

weights_df.to_csv('taxcalc/pit_weights_macedonia.csv', index=False)










