"""
app00.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app00.py > app00.res
CHECK: Use your favorite Windows diff utility to confirm that app00.res is
       the same as the app00.out file that is in the repository.
"""
import pandas as pd
import matplotlib.pyplot as plt
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

grecs = GSTRecords()

# create CorpRecords object using cross-section data
crecs1 = CorpRecords(data='cit_poland.csv', weights='cit_weights_poland.csv')
# Note: weights argument is optional
assert isinstance(crecs1, CorpRecords)
assert crecs1.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator objects for current-law policy
calc1 = Calculator(policy=pol, records=recs, corprecords=crecs1,
                   gstrecords=grecs, verbose=False)
pol2 = Policy()
reform = Calculator.read_json_param_objects('app01_reform.json', None)
pol2.implement_reform(reform['policy'])

calc2 = Calculator(policy=pol2, records=recs, corprecords=crecs1,
                   gstrecords=grecs, verbose=False)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017

np.seterr(divide='ignore', invalid='ignore')

# Produce DataFrame of results using cross-section
calc1.calc_all()
calc2.calc_all()
#sector=calc1.carray('sector')

dump_vars = ['legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
             'income_tax_base_after_deductions', 'citax']
dumpdf_2017 = calc1.dataframe_cit(dump_vars)
dumpdf_2017.to_csv('app00_poland.csv', index=False, float_format='%.0f')

Tax_Base_Before_Deductions = calc1.carray('tax_base_before_deductions')
Deductions = calc1.carray('deductions_from_tax_base')
Tax_Base_After_Deductions = calc1.carray('income_tax_base_after_deductions')
citax = calc1.carray('citax')
weight = calc1.carray('weight')
etr = np.divide(citax, Tax_Base_Before_Deductions)
weighted_etr = etr*weight.values
weighted_etr_overall = sum(weighted_etr[~np.isnan(weighted_etr)])/sum(weight.values[~np.isnan(weighted_etr)])
#sector = calc1.carray('sector')

wtd_citax = citax * weight

citax_collection1 = wtd_citax.sum()

citax_collection_billions1 = citax_collection1/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2017\n')

print("The CIT Collection in billions Current Law is: ", citax_collection_billions1)

dumpdf_2017 = calc2.dataframe_cit(dump_vars)
dumpdf_2017.to_csv('app00_poland.csv', index=False, float_format='%.0f')

Tax_Base_Before_Deductions = calc2.carray('tax_base_before_deductions')
Deductions = calc2.carray('deductions_from_tax_base')
Tax_Base_After_Deductions = calc2.carray('income_tax_base_after_deductions')
citax = calc2.carray('citax')
weight = calc2.carray('weight')
etr = np.divide(citax, Tax_Base_Before_Deductions)
weighted_etr = etr*weight.values
weighted_etr_overall = sum(weighted_etr[~np.isnan(weighted_etr)])/sum(weight.values[~np.isnan(weighted_etr)])
#sector = calc1.carray('sector')

wtd_citax = citax * weight

citax_collection2 = wtd_citax.sum()

citax_collection_billions2 = citax_collection2/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2017\n')

print("The CIT Collection in billions after Reform is: ", citax_collection_billions2)

citax_difference = citax_collection2 - citax_collection1

print("The CIT Collection difference: ", citax_difference)

