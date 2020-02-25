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
def corp_tax_base_before_deductions(tax_base_before_deductions, 
                            deductions_from_tax_base,
                            income_tax_base_after_deductions):
    """
    Compute corp tax base after taking out the deductions.
    """
    income_tax_base_after_deductions = (tax_base_before_deductions -
                                        deductions_from_tax_base)
    print(tax_base_before_deductions)
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
