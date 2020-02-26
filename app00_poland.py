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
                   gstrecords=grecs)

# NOTE: calc1 now contains a PRIVATE COPY of pol and a PRIVATE COPY of recs,
#       so we can continue to use pol and recs in this script without any
#       concern about side effects from Calculator method calls on calc1.

assert isinstance(calc1, Calculator)
assert calc1.current_year == 2017

np.seterr(divide='ignore', invalid='ignore')

# Produce DataFrame of results using cross-section
calc1.calc_all()

#sector=calc1.carray('sector')

Tax_Base_Before_Deductions = calc1.carray('tax_base_before_deductions')
Deductions = calc1.carray('deductions_from_tax_base')
Tax_Base_After_Deductions = calc1.carray('income_tax_base_after_deductions')
citax = calc1.carray('citax')

weight = calc1.carray('weight')
etr = np.divide(citax, Tax_Base_Before_Deductions)
weighted_etr = etr*weight.values
weighted_etr_overall = sum(weighted_etr[~np.isnan(weighted_etr)])/sum(weight.values[~np.isnan(weighted_etr)])
#sector = calc1.carray('sector')

print('\n\n\n')
print(f'Tax Base Before Deductions, 2017: {sum(Tax_Base_Before_Deductions * weight) / 10**9:,.2f} Billion')
print(f'Deductions, 2017: {sum(Deductions * weight) / 10**9:,.2f} Billion')
print(f'Tax Base After Deductions, 2017: {sum(Tax_Base_After_Deductions * weight) / 10**9:,.2f} Billion')
print(f'CIT Collection, 2017: {sum(citax * weight) / 10**9:,.2f} Billion')
print(f'Effective Tax Rate, 2017: {weighted_etr_overall*100:,.1f}%')

print('\n\n\n')

dump_vars = ['legal_form', 'sector', 'tax_base_before_deductions', 'deductions_from_tax_base',
             'income_tax_base_after_deductions', 'citax']
dumpdf = calc1.dataframe_cit(dump_vars)
dumpdf.to_csv('app00_poland.csv', index=False, float_format='%.0f')

df_sector = dumpdf.groupby(['sector']).sum()
df_sector['citax_millions'] = df_sector['citax']/10**6
ax = df_sector.plot(kind='bar', use_index=True, y='citax_millions', 
                    yticks = np.linspace(0,7,15), legend=False, rot=90)

ax.set_ylabel('CIT in million Zlotys')
ax.set_xlabel('')
plt.show()
"""
calc1.increment_year()
calc1.calc_all()
"""