"""
app00.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app00.py > app00.res
CHECK: Use your favorite Windows diff utility to confirm that app00.res is
       the same as the app00.out file that is in the repository.
"""
import pandas as pd
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
                   gstrecords=grecs)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017

np.seterr(divide='ignore', invalid='ignore')

# Produce DataFrame of results using cross-section
calc1.calc_all()
Tax_Base_Before_Deductions = calc1.carray('tax_base_before_deductions')
Deductions = calc1.carray('deductions_from_tax_base')
Tax_Base_After_Deductions = calc1.carray('income_tax_base_after_deductions')
citax = calc1.carray('citax')

weight = calc1.carray('weight')
etr = np.divide(citax, Tax_Base_Before_Deductions)
etr[~np.isfinite(etr)] = 0
weighted_etr = sum(etr*weight.values/sum(weight.values))

"""
calc1.increment_year()
calc1.calc_all()
AggInc18c = calc1.carray('GTI_Before_Loss')
GTI18c = calc1.carray('deductions')
citax18c = calc1.carray('citax')
citax18c_with_MAT = calc1.carray('citax_after_MAT')
wgt18c = calc1.carray('weight')
etr18c = np.divide(citax18c_with_MAT,AggInc18c)
etr18c[~np.isfinite(etr18c)] = 0
wtd_etr18c = sum(etr18c*wgt18c.values/sum(wgt18c.values))
results_cross = pd.DataFrame({'Aggregate_Income2017': AggInc17c,
                              'citax2017': citax17c,
                              'Aggregate_Income2018': AggInc18c,
                              'citax2018': citax18c})
results_cross.to_csv('app00-dump-crosssection.csv', index=False,
                     float_format='%.0f')
"""

print('\n\n\n')
print(f'Tax Base Before Deductions, 2017: {sum(Tax_Base_Before_Deductions * weight) / 10**9:,.0f} Billion')
print(f'Deductions, 2017: {sum(Deductions * weight) / 10**9:,.0f} Billion')
print(f'Tax Base After Deductions, 2017: {sum(Tax_Base_After_Deductions * weight) / 10**9:,.0f} Billion')
print(f'CIT Collection, 2017: {sum(citax * weight) / 10**9:,.0f} Billion')
print(f'Effective Tax Rate, 2017: {weighted_etr*100:,.1f}%')

print('\n\n\n')

"""
print(f'GTI before loss, 2018, cross-section: {sum(AggInc18c * wgt18c) / 10**9:,.0f} Billion')
print(f'Deductions, 2018, cross-section: {sum(GTI18c * wgt18c) / 10**9:,.0f} Billion')
print(f'Total liability, 2018, cross-section: {sum(citax18c * wgt18c) / 10**9:,.0f} Billion')
print(f'Total liability with MAT, 2018, cross-section: {sum(citax18c_with_MAT * wgt18c) / 10**9:,.0f} Billion')
print(f'Effective Tax Rate, 2018, cross-section: {wtd_etr18c*100:,.1f}%')
print('\n\n\n')


print('GTI before loss, 2017, cross-section: ' +
      str(sum(AggInc17c * wgt17c) / 10**7))
print('Deductions, 2017, cross-section: ' +
      str(sum(GTI17c * wgt17c) / 10**7))
print('Total liability, 2017, cross-section: ' +
      str(sum(citax17c * wgt17c) / 10**7))
print('Total liability with MAT, 2017, cross-section: ' +
      str(sum(citax17c_with_MAT * wgt17c) / 10**7))
print('Tax rate, 2017, cross-section: ' +
      str(sum(citax17c * wgt17c) / sum(GTI17c * wgt17c)))
print('\n')
print('GTI before loss, 2017, panel: ' +
      str(sum(AggInc17p * wgt17p) / 10**7))
print('Deductions, 2017, panel: ' +
      str(sum(GTI17p * wgt17p) / 10**7))
print('Total liability, 2017, panel: ' +
      str(sum(citax17p * wgt17p) / 10**7))
print('Total liability with MAT, 2017, panel: ' +
      str(sum(citax17p_with_MAT * wgt17p) / 10**7))
print('Tax rate, 2017, panel: ' +
      str(sum(citax17p * wgt17p) / sum(GTI17p * wgt17p)))
print('\n')
print('GTI before loss, 2018, cross-section: ' +
      str(sum(AggInc18c * wgt18c) / 10**7))
print('Deductions, 2018, cross-section: ' + str(sum(GTI18c * wgt18c) / 10**7))
print('Total liability, 2018, cross-section: ' +
      str(sum(citax18c * wgt18c) / 10**7))
print('Total liability with MAT, 2018, cross-section: ' +
      str(sum(citax18c_with_MAT * wgt17c) / 10**7))
print('Tax rate, 2018, cross-section: ' +
      str(sum(citax18c * wgt18c) / sum(GTI18c * wgt18c)))
print('\n')
print('GTI before loss, 2018, panel: ' + str(sum(AggInc18p * wgt18p) / 10**7))
print('Deductions, 2018, panel: ' + str(sum(GTI18p * wgt18p) / 10**7))
print('Total liability, 2018, panel: ' + str(sum(citax18p * wgt18p) / 10**7))
print('Total liability with MAT, 2018, panel: ' +
      str(sum(citax18p_with_MAT * wgt18p) / 10**7))
print('Tax rate, 2018, panel: ' +
      str(sum(citax18p * wgt18p) / sum(GTI18p * wgt18p)))
print('\n')
print('Average liability, 2017, cross-section: ' +
      str(sum(citax17c * wgt17c) / sum(wgt17c) / 10**7))
print('Average liability, 2017, panel: ' +
      str(sum(citax17p * wgt17p) / sum(wgt17p) / 10**7))
"""