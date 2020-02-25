"""
Functions that calculate GST paid.
"""
# CODING-STYLE CHECKS:
# pycodestyle gstfunctions.py
# pylint --disable=locally-disabled gstfunctions.py

import math
import copy
import json
import numpy as np
from taxcalc.decorators import iterate_jit

DEBUG = False
DEBUG_IDX = 0

@iterate_jit(nopython=True)
def gst_liability(gst_rate, CONSUMPTION_TOTAL, gst):
    gst = gst_rate*CONSUMPTION_TOTAL
    return (gst)





