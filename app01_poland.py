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

dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
             'income_tax_base_after_deductions', 'citax']
dumpdf_2017 = calc1.dataframe_cit(dump_vars)
dumpdf_2017.to_csv('app00_poland2017.csv', index=False, float_format='%.0f')

citax_2017 = calc1.carray('citax')
weight_2017 = calc1.carray('weight')

wtd_citax_2017 = citax_2017 * weight_2017

citax_collection_2017 = wtd_citax_2017.sum()

citax_collection_billions_2017 = citax_collection_2017/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2017\n')

print("The CIT Collection in billions is: ", citax_collection_billions_2017)

calc1.increment_year()
calc1.calc_all()

citax_2018 = calc1.carray('citax')
weight_2018 = calc1.carray('weight')

wtd_citax_2018 = citax_2018 * weight_2018

citax_collection_2018 = wtd_citax_2018.sum()

citax_collection_billions_2018 = citax_collection_2018/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2018\n')

print("The CIT Collection in billions is: ", citax_collection_billions_2018)

calc1.increment_year()
calc1.calc_all()

citax_2019 = calc1.carray('citax')
weight_2019 = calc1.carray('weight')

wtd_citax_2019 = citax_2019 * weight_2019

citax_collection_2019 = wtd_citax_2019.sum()

citax_collection_billions_2019 = citax_collection_2019/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2019\n')

print("The CIT Collection in billions is: ", citax_collection_billions_2019)

calc1.advance_to_year(2020)
calc1.calc_all()

citax_2020 = calc1.carray('citax')
weight_2020 = calc1.carray('weight')

wtd_citax_2020 = citax_2020 * weight_2020

citax_collection_2020 = wtd_citax_2020.sum()

citax_collection_billions_2020 = citax_collection_2020/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2020\n')

print("The CIT Collection in billions is: ", citax_collection_billions_2020)