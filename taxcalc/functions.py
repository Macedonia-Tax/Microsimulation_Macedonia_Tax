"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

@iterate_jit(nopython=True)
def cal_OLESNUVANJE1(K_Tax_Relief,OLESNUVANJE1):
    OLESNUVANJE1 = K_Tax_Relief*1.072961373390
    return(OLESNUVANJE1)
    
@iterate_jit(nopython=True)
def cal_MINUS_DANOCNA_OSNOVA(OLESNUVANJE1, K_Tax_Relief, MINUS_DANOCNA_OSNOVA):
    MINUS_DANOCNA_OSNOVA = OLESNUVANJE1 - K_Tax_Relief
    return(MINUS_DANOCNA_OSNOVA)
    

@iterate_jit(nopython=True)
def net_salary_income(Salaries, MINUS_DANOCNA_OSNOVA, Income_Salary):
    """
    Compute net salary as gross salary minus deductions u/s 16.
    """
    # TODO: when gross salary and deductions are avaiable, do the calculation
    # TODO: when using net_salary as function argument, no calculations neeed
    """
    The deductions (transport and medical) that are being done away with while
    intrducing Standard Deduction is not captured in the schedule also. Thus,
    the two deductions combined (crude estimate gives a figure of 30000) is
    added to "SALARIES" and then "std_deduction" (introduced as a policy
    variable) is deducted to get "Income_Salary". Standard Deduction is being
    intruduced only from AY 2019 onwards, "std_deduction" is set as 30000 for
    AY 2017 and of 2018 thus resulting in no change for those years.
    """
    if (Salaries == 0):
        DANOCNA_OSNOVA_0 = 0
    else:    
        DANOCNA_OSNOVA_0 = Salaries-MINUS_DANOCNA_OSNOVA
    Income_Salary = DANOCNA_OSNOVA_0 
    return Income_Salary
  
@iterate_jit(nopython=True)
def gross_total_income(Income_Salary, GTI):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    GTI = Income_Salary
    return GTI


@iterate_jit(nopython=True)
def taxable_total_income(GTI, TTI):
    """
    Compute TTI.
    """
    TTI = GTI 
    return TTI    


@iterate_jit(nopython=True)
def pit_liability(rate1, rate2, tbrk1, TTI, pitax):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = TTI 
    tax = (rate1 * min(taxinc, tbrk1) +
                       rate2 * max(0., taxinc - tbrk1))
    pitax = tax 
    return (pitax)


import pandas as pd
data = pd.read_csv (r'C:\Users\wb544155\OneDrive - WBG\Documents\GitHub\Microsimulation_Macedonia_Tax\calc_gini.csv')
print (data)
gini = pd.DataFrame(data, columns= ['id','Salaries'])

@iterate_jit(nopython=True)
def gini_coefficient(gini):
    
        """
    Compute gini-index
      
    """ 
    gini['weight'] = 100
    gini['cumulative_weight']=np.cumsum(gini['weight'])
    sum_weight = (gini['weight']).sum()
    gini['percentage_cumul_pop'] = gini['cumulative_weight']/sum_weight
    gini['total_income'] = gini['weight']*gini['Salaries']
    gini['cumulative_total_income']= np.cumsum(gini['total_income'])
    sum_total_income = sum(gini['total_income'])
    gini['percentage_cumul_income'] = gini['cumulative_total_income']/sum_total_income
    gini['height'] = gini['percentage_cumul_pop']-gini['percentage_cumul_income']
    gini['lag_percentage_cumul_pop']= gini['percentage_cumul_pop'].shift(1)
    gini['lag_percentage_cumul_income']= gini['percentage_cumul_income'].shift(1)
    gini['lag_height']= gini['height'].shift(1)
    gini['lag_percentage_cumul_pop']= gini['lag_percentage_cumul_pop'].fillna(0)
    gini['lag_percentage_cumul_income']= gini['lag_percentage_cumul_income'].fillna(0)
    gini['lag_height']= gini['lag_height'].fillna(0)
    gini['base'] = gini.lag_percentage_cumul_pop.diff()
    gini['base']= gini['base'].fillna(0)
    gini['integrate_area']= 0.5*gini['base']*(gini['height']+gini['height'].shift())
    sum_integrate_area = gini['integrate_area'].sum()
    gini_index = 2*(sum_integrate_area)
    return(gini_index)
    
    
    
    
   
    




 #to create a lag variable
#df['lagprice'] = df['price'].shift(1)
#For a single column using pandas: 
#df['DataFrame Column'] = df['DataFrame Column'].fillna(0)
#For a single column using numpy:
#df['DataFrame Column'] = df['DataFrame Column'].replace(np.nan, 0)   
    
    






