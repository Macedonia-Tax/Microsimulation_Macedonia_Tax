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


"Calculation for wages" 
@iterate_jit(nopython=True)
def cal_ssc_w(ssc_rate_w, gross_i_w, ssc_w):
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
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    ssc_w = ssc_rate_w*gross_i_w
    return ssc_w

@iterate_jit(nopython=True)
def cal_tti_w(gross_i_w, ssc_w, personal_allowance_w, tti_w):
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
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    tti_w = gross_i_w - ssc_w - personal_allowance_w 
    return tti_w

@iterate_jit(nopython=True)
def cal_pit_w(rate1, rate2, tbrk1, tti_w, pit_w):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tti_w 
    tax = (rate1 * min(taxinc, tbrk1) +
                       rate2 * max(0., taxinc - tbrk1))
    pit_w = tax 
    return (pit_w)


@iterate_jit(nopython=True)
def cal_net_i_w(gross_i_w, ssc_w, pit_w):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    net_i_w = gross_i_w- ssc_w- pit_w 
    return net_i_w


"Calculation for Other Income of Labor"
@iterate_jit(nopython=True)
def cal_ssc_I(ssc_rate_I, gross_i_I, ssc_I):
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
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    ssc_I = ssc_rate_I*gross_i_I
    return ssc_I

@iterate_jit(nopython=True)
def cal_tti_I(gross_i_I, ssc_I, personal_allowance_I, deductions_I, tti_I):
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
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    tti_I = gross_i_I - deductions_I- ssc_I - personal_allowance_I 
    return tti_I

@iterate_jit(nopython=True)
def cal_pit_I(rate1, rate2, tbrk1, tti_I, pit_I):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tti_I 
    tax = (rate1 * min(taxinc, tbrk1) +
                       rate2 * max(0., taxinc - tbrk1))
    pit_I = tax 
    return (pit_I)


@iterate_jit(nopython=True)
def cal_net_i_I(gross_i_I, ssc_I, pit_I, net_i_I):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    net_i_I = gross_i_I - pit_I- ssc_I
    return net_i_I
 
    
"Calculation for Income from Capital"
@iterate_jit(nopython=True)
def cal_tti_c(gross_i_c, deductions_c, tti_c):
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
    intruduced only from AY 2021 onwards, "std_deduction" is set as 30000 for
    AY 2019 and of 2020 thus resulting in no change for those years.
    """

    tti_c = gross_i_c - deductions_c 
    return tti_c

@iterate_jit(nopython=True)
def cal_pit_c(capital__income_rate, tti_c, pit_c):
    """pit_c
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    pit_c = capital__income_rate*tti_c
    return pit_c

@iterate_jit(nopython=True)
def cal_net_i_c(gross_i_c, pit_c, net_i_c):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    net_i_c = gross_i_c - pit_c   
    return net_i_c


"total"
@iterate_jit(nopython=True)
def cal_total_gross_income(gross_i_w, gross_i_I, gross_i_c, total_gross_income):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    total_gross_income = gross_i_w + gross_i_I + gross_i_c
    return total_gross_income

@iterate_jit(nopython=True)
def cal_total_taxable_income(tti_w, tti_I, tti_c, total_taxable_income):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    total_taxable_income = tti_w + tti_I + tti_c
    return total_taxable_income

@iterate_jit(nopython=True)
def cal_total_pit(pit_w, pit_I, pit_c, total_pit):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    total_pit = pit_w + pit_I + pit_c
    return total_pit

@iterate_jit(nopython=True)
def cal_total_net_icome(net_i_w, net_i_I, net_i_c, total_net_icome):
    """
    Compute GTI including capital gains amounts taxed at special rates.
    """
    total_net_icome = net_i_w + net_i_I + net_i_c
    return total_net_icome







