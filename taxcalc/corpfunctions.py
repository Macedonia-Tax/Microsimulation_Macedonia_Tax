"""
Functions that calculate corporate income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle corpfunctions.py
# pylint --disable=locally-disabled corpfunctions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

@iterate_jit(nopython=True)
def corp_income(revenue, expenditure, income, loss):
    """
    Compute Income = Revenue - Expenditure
    """
    if (revenue >= expenditure):
        income = revenue - expenditure
        loss = 0
    else:
        loss = -(revenue - expenditure)
        income=0
    
    return (income, loss)

@iterate_jit(nopython=True)
def corp_tax_base_before_deductions(income, tax_free_income_total,
                                    deductions_from_income_total,
                                    tax_base_before_deductions):
    """
    Compute corp tax base after taking out the deductions.
    """
    tax_base_before_deductions = (income - tax_free_income_total -
                                  deductions_from_income_total)
   
    return (tax_base_before_deductions)

@iterate_jit(nopython=True)
def corp_tax_base_after_deductions(tax_base_before_deductions,
                            deductions_from_tax_base,
                            income_tax_base_after_deductions):
    """
    Compute corp tax base after taking out the deductions.
    """
    income_tax_base_after_deductions = (tax_base_before_deductions -
                                        deductions_from_tax_base)
    return (income_tax_base_after_deductions)

@iterate_jit(nopython=True)
def cit_liability(cit_rate_regular, income_tax_base_after_deductions, citax):
    """
    Compute tax liability given the tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)

    """
    # compute citax amount
    citax = cit_rate_regular * income_tax_base_after_deductions
    return (citax)
