"""
app1.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app1.py > app1.res
CHECK: Use your favorite Windows diff utility to confirm that app1.res is
       the same as the app1.out file that is in the repository.
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create GSTRecords object containing gst.csv and gst_weights.csv input data
grecs = GSTRecords()

assert isinstance(grecs, GSTRecords)
assert grecs.data_year == 2017
assert grecs.current_year == 2017

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

assert isinstance(crecs, CorpRecords)
assert crecs.data_year == 2017
assert crecs.current_year == 2017

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc1.calc_all()

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app1_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)
calc2.calc_all()

# compare aggregate results from two calculators
weighted_tax1 = calc1.weighted_total('pitax')
weighted_tax2 = calc2.weighted_total('pitax')
total_weights = calc1.total_weight()
print(f'Tax 1 {weighted_tax1 * 1e-6:,.2f}')
print(f'Tax 2 {weighted_tax2 * 1e-6:,.2f}')
print(f'Total weight {total_weights * 1e-6:,.2f}')


import pandas as pd
data = pd.read_csv (r'C:\Users\wb544155\OneDrive - WBG\Documents\GitHub\Microsimulation_Macedonia_Tax\calc_gini.csv')
print (data)
gini = pd.DataFrame(data, columns= ['id','Salaries'])
gini['weight'] = 100
gini['cumulative_weight']=np.cumsum(gini['weight'])
sum_weight = (gini['weight']).sum()
gini['percentage_cumul_pop'] = gini['cumulative_weight']/sum_weight
gini['total_income'] = gini['weight']*gini['Salaries']
gini['cumulative_total_income']= np.cumsum(gini['total_income'])
sum_total_income = sum(gini['total_income'])
gini['percentage_cumul_income'] = gini['cumulative_total_income']/sum_total_income
gini['height'] = gini['percentage_cumul_pop']-gini['percentage_cumul_income']
gini['lag_percentage_cumul_pop']= gini['percentage_cumul_pop'].shift(1)
gini['lag_percentage_cumul_income']= gini['percentage_cumul_income'].shift(1)
gini['lag_height']= gini['height'].shift(1)
gini['lag_percentage_cumul_pop']= gini['lag_percentage_cumul_pop'].fillna(0)
gini['lag_percentage_cumul_income']= gini['lag_percentage_cumul_income'].fillna(0)
gini['lag_height']= gini['lag_height'].fillna(0)
gini['base'] = gini.lag_percentage_cumul_pop.diff()
gini['base']= gini['base'].fillna(0)
gini['integrate_area']= 0.5*gini['base']*(gini['height']+gini['height'].shift())
sum_integrate_area = gini['integrate_area'].sum()
gini_index = 2*(sum_integrate_area)


#ploting gini coefficient
import numpy as np
import matplotlib.pyplot as plt

n = 430
w = np.exp(np.random.randn(n))

f_vals = gini['lag_percentage_cumul_pop']
l_vals = gini['lag_percentage_cumul_income']

fig, ax = plt.subplots()
ax.plot(f_vals, l_vals, label='Lorenz curve, lognormal sample')
ax.plot(f_vals, f_vals, label='Line of Equality, 45 degrees')
ax.legend()
plt.show()


"""
#compare pre-tax-gini and pro-tax-gini
pre_reform_gini = calc1.('gini_index')
pro_reform_gini = calc2.('gini_index')
"""


# Show results from corporate tax
print(calc1.carray('NET_TAX_LIABILTY'))
print(calc2.carray('NET_TAX_LIABILITY_A'))

# dump out records
dump_vars = ['ID_No','Salaries', 'GTI', 'TTI', 'pitax']
dumpdf = calc1.dataframe(dump_vars)
dumpdf['pitax1'] = calc1.array('pitax')
dumpdf['pitax2'] = calc2.array('pitax')
dumpdf['pitax_diff'] = dumpdf['pitax2'] - dumpdf['pitax1']
column_order = dumpdf.columns

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app1-dump.csv', columns=column_order,
              index=False, float_format='%.0f')
