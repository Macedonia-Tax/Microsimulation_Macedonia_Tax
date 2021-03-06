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
def cal_ssc(ssc_rate, Gross_income, Social_Security_Contributions):
    """
    Compute ssc as gross salary minus deductions u/s 16.
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

    Social_Security_Contributions = ssc_rate*Gross_income
    return Social_Security_Contributions

@iterate_jit(nopython=True)
def net_salary_income(Gross_income, Social_Security_Contributions, Tax_Relief,
                      Income_Salary):
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

    Income_Salary = Gross_income-Social_Security_Contributions-Tax_Relief
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


@iterate_jit(nopython=True)
def cal_post_tax_income(GTI,pitax,post_tax_income):
    """
    Calculating post tax income
    """
    post_tax_income = GTI-pitax
    return(post_tax_income)
    
    






