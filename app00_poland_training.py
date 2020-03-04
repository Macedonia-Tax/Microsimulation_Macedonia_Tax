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
dumpdf_1.to_csv('app00_poland_output1.csv', index=False, float_format='%.0f')

citax1 = calc1.carray('citax')
weight1 = calc1.carray('weight')

wtd_citax1 = citax1 * weight1
citax_collection1 = wtd_citax1.sum()
citax_collection_billions1 = citax_collection1/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2017\n')
print("The CIT Collection under Current Law is: ",
      citax_collection_billions1, "billions")

"{:.2f}".format(citax_collection_billions1)
print("{:.2f}".format(citax_collection_billions1))
print("The CIT Collection under Current Law is: " +
      "{:.2f}".format(citax_collection_billions1), "billions")


dump_vars = ['CIT_ID_NO', 'legal_form', 'sector', 'province', 'small_business', 'revenue', 'expenditure', 'income', 'tax_base_before_deductions', 'deductions_from_tax_base',
             'income_tax_base_after_deductions', 'citax']
dumpdf_2 = calc2.dataframe_cit(dump_vars)
dumpdf_2.to_csv('app00_poland_output2.csv', index=False, float_format='%.0f')

citax2 = calc2.carray('citax')
weight2 = calc2.carray('weight')

wtd_citax2 = citax2 * weight2
citax_collection2 = wtd_citax2.sum()
citax_collection_billions2 = citax_collection2/10**9

print('\n\n\n')
print('TAX COLLECTION FOR THE YEAR - 2017\n')
print("The CIT Collection under Reform is: ",
      citax_collection_billions2, "billions")

print("The CIT Collection under Current Law is: " +
      "{:.2f}".format(citax_collection_billions2), "billions")

cit_collection_difference_millions = ((citax_collection2 - citax_collection1)/
                                      10**6)


print('\n\n\n')
print("The Difference in CIT Collection due to Reform is: ",
      cit_collection_difference_millions, "millions")
print("The Difference in CIT Collection due to Reform is: " +
      "{:.2f}".format(cit_collection_difference_millions), "millions")
print('\n\n\n')


df_sector = dumpdf_1.groupby(['sector']).sum()
df_sector['citax_millions'] = df_sector['citax']/10**6

df_sector.plot.bar(y='citax')

cmap = plt.cm.tab10
colors = cmap(np.arange(len(df_sector)) % cmap.N)

ax = df_sector.plot(kind='bar', use_index=True, y='citax_millions', 
                    yticks = np.linspace(0,7,15), legend=False, rot=90,
                    figsize=(8,8), color=colors)
ax.set_ylabel('CIT in million Zlotys')
ax.set_xlabel('')
ax.set_title(' CIT collection by Sector (2017)', fontweight="bold")
plt.show()



df_small_business = dumpdf_1.groupby(['small_business']).sum()
df_small_business['citax_millions'] = df_sector['citax']/10**6

df_small_business.plot.pie(y='citax')

Business_Profit1 = calc1.carray('income')
etr1 = np.divide(citax1, Business_Profit1)
weighted_etr1 = etr1*weight1.values
weighted_etr_overall1 = (sum(weighted_etr1[~np.isnan(weighted_etr1)])/
                         sum(weight1.values[~np.isnan(weighted_etr1)]))

print("Effective Tax Rate Overall:", weighted_etr_overall1)

