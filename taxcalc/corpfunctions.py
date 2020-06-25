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
def cit_liability(cit_rate, CIT_Income, citax):
    """
    Compute tax liability given the tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # compute citax amount
    citax = cit_rate * CIT_Income

    return (citax)
