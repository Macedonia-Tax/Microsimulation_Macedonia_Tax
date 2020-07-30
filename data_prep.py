# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:04:25 2020

@author: WB544155
"""

import pandas as pd
import numpy as np


sample_data = pd.read_csv("taxcalc/macedonia_merged_data.csv")
return_data = pd.read_csv("macedonia_return_pop.csv")


return_list = ['1','1b','1g','1v','2','3','5','6','8','9','10','11','13','14']
for return_no in return_list:
    sample_total= sample_data[sample_data['return_no']==return_no]['Gross_income'].sum()
    population_total= return_data[return_data['return_no']==return_no]['total_gross_income'].values[0]
    weight= population_total/sample_total
    return_data['weight'] = np.where(return_data['return_no']==return_no, weight, return_data['weight'])
    
weights_df = sample_data[['return_no']]
weights_df= pd.merge(weights_df,return_data,how='left',on='return_no')
weights_df= weights_df[['weight']]
weights_df = weights_df.rename(columns={'weight':'WT2017'})

growth_rate_tax_filers = 0

weights_df['WT2018'] = weights_df['WT2017'] * (1+growth_rate_tax_filers)
weights_df['WT2019'] = weights_df['WT2018'] * (1+growth_rate_tax_filers)
weights_df['WT2020'] = weights_df['WT2019'] * (1+growth_rate_tax_filers)
weights_df['WT2021'] = weights_df['WT2020'] * (1+growth_rate_tax_filers)
weights_df['WT2022'] = weights_df['WT2021'] * (1+growth_rate_tax_filers)
weights_df['WT2023'] = weights_df['WT2022'] * (1+growth_rate_tax_filers)
weights_df = weights_df.fillna(1000)
weights_df.to_csv('taxcalc/pit_weights_macedonia.csv', index=False)




