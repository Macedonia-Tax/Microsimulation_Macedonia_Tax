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
dumpdf_1 = calc1.dataframe_cit(dump_vars)
dumpdf_1.to_csv('app00_poland1.csv', index=False, float_format='%.0f')

Business_Profit1 = calc1.carray('income')
Tax_Free_Incomes1 = calc1.carray('tax_free_income_total')
Tax_Base_Before_Deductions1 = calc1.carray('tax_base_before_deductions')
Deductions1 = calc1.carray('deductions_from_tax_base')
Tax_Base_After_Deductions1 = calc1.carray('income_tax_base_after_deductions')
citax1 = calc1.carray('citax')
weight1 = calc1.carray('weight')
etr1 = np.divide(citax1, Business_Profit1)
weighted_etr1 = etr1*weight1.values
weighted_etr_overall1 = (sum(weighted_etr1[~np.isnan(weighted_etr1)])/
                         sum(weight1.values[~np.isnan(weighted_etr1)]))

wtd_citax1 = citax1 * weight1

citax_collection1 = wtd_citax1.sum()

citax_collection_billions1 = citax_collection1/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2017\n')

print("The CIT Collection in billions is: ", citax_collection_billions1)

dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
             'income_tax_base_after_deductions', 'citax']
dumpdf_2 = calc2.dataframe_cit(dump_vars)
dumpdf_2.to_csv('app00_poland2.csv', index=False, float_format='%.0f')

Business_Profit2 = calc2.carray('income')
Tax_Free_Incomes2 = calc2.carray('tax_free_income_total')
Tax_Base_Before_Deductions2 = calc2.carray('tax_base_before_deductions')
Deductions2 = calc2.carray('deductions_from_tax_base')
Tax_Base_After_Deductions2 = calc2.carray('income_tax_base_after_deductions')
citax2 = calc2.carray('citax')
weight2 = calc2.carray('weight')
etr2 = np.divide(citax2, Business_Profit2)
weighted_etr2 = etr2*weight2.values
weighted_etr_overall2 = (sum(weighted_etr2[~np.isnan(weighted_etr2)])/
                         sum(weight2.values[~np.isnan(weighted_etr2)]))

wtd_citax2 = citax2 * weight2

citax_collection2 = wtd_citax2.sum()

citax_collection_billions2 = citax_collection2/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2017-Reform\n')

print("The CIT Collection in billions is: ",citax_collection_billions2)

print("Difference due to change in policy in small businesses:",(citax_collection_billions2 - citax_collection_billions1)*10**3,"millions")

"""
print('\n\n\n')
print('FORECASTING TAX COLLECTION FOR THE FOLLOWING YEAR - 2018\n')
print(f'CIT Collection, 2018: {sum(citax * weight) / 10**9:,.2f} Billion')

print(f'Tax Base Before Deductions, 2018: {sum(Tax_Base_Before_Deductions * weight) / 10**9:,.2f} Billion')
print(f'Deductions, 2018: {sum(Deductions * weight) / 10**9:,.2f} Billion')
print(f'Tax Base After Deductions, 2018: {sum(Tax_Base_After_Deductions * weight) / 10**9:,.2f} Billion')
print(f'Effective Tax Rate, 2018: {weighted_etr_overall*100:,.1f}%')
"""

df_sector = dumpdf_1.groupby(['sector']).sum()
df_sector['citax_millions'] = df_sector['citax']/10**6

df_province = dumpdf_1.groupby(['province']).sum()
df_province['citax_millions'] = df_province['citax']/10**6

df_small_business = dumpdf_1.groupby(['small_business']).sum()
df_small_business['citax_millions'] = df_small_business['citax']/10**6

cmap = plt.cm.tab10
colors = cmap(np.arange(len(df_sector)) % cmap.N)

ax = df_sector.plot(kind='bar', use_index=True, y='citax_millions', 
                    yticks = np.linspace(0,7,15), legend=False, rot=90,
                    figsize=(8,8), color=colors)

ax.set_ylabel('CIT in million Zlotys')
ax.set_xlabel('')
ax.set_title(' CIT collection by sector (2017)', fontweight="bold")
plt.show()

cmap = plt.cm.tab10
colors = cmap(np.arange(len(df_province)) % cmap.N)

ax = df_province.plot(kind='bar', use_index=True, y='citax_millions', 
                    yticks = np.linspace(0,7,15), legend=False, rot=90,
                    figsize=(8,8), color=colors)
ax.set_ylabel('CIT in million Zlotys')
ax.set_xlabel('')
ax.set_title(' CIT collection by Province (2017)', fontweight="bold")
plt.show()

cmap = plt.cm.tab10
colors = cmap(np.arange(len(df_province)) % cmap.N)

ax = df_small_business.plot(kind='bar', use_index=True, y='citax_millions', 
                    yticks = np.linspace(0,7,15), legend=False, rot=90,
                    figsize=(8,8), color=colors)
ax.set_ylabel('CIT in million Zlotys')
ax.set_xlabel('')
ax.set_title(' CIT collection by Type of Business (2017)', fontweight="bold")
plt.show()


