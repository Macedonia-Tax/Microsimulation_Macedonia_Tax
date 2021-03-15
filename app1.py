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
assert grecs.data_year == 2019
assert grecs.current_year == 2019

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

assert isinstance(crecs, CorpRecords)
assert crecs.data_year == 2019
assert crecs.current_year == 2019

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
weighted_tax1 = calc1.weighted_total('total_pit')
weighted_tax2 = calc2.weighted_total('total_pit')
weighted_tax_diff = weighted_tax2 - weighted_tax1
total_weights = calc1.total_weight()
print(f'Tax under current law {weighted_tax1 * 1e-6:,.2f} millions')
print(f'Tax under reform {weighted_tax2 * 1e-6:,.2f} millions')
print(f'Tax difference {weighted_tax_diff * 1e-6:,.2f} millions')
print(f'Total number of tax returns {total_weights * 1e-6:,.2f} millions')


dump_vars = ['id_n','total_gross_income','total_taxable_income','total_pit','total_net_icome']
dumpdf = calc1.dataframe(dump_vars)
dumpdf= dumpdf.sort_values(by=['total_gross_income'])
dumpdf.to_csv('app1-dump_macedonia.csv',
              index=False, float_format='%.0f')


gini_pre_tax = calc1.gini(['total_gross_income'])
print(gini_pre_tax)

gini_post_tax = calc1.gini(['total_net_icome'])
print(gini_post_tax)

gini_post_tax_reform = calc2.gini(['total_net_icome'])
print(gini_post_tax_reform)


"""
import matplotlib as plt
output_categories = 'Gross_income'
dt1, dt2 = calc1.distribution_tables(calc2, output_categories, averages = True, scaling = True)
dt1 = dt1.fillna(0)
print(dt1)
dt2['pitax_diff'] = dt2['pitax'] - dt1['pitax']
dt2['etr'] = (dt2['pitax']/dt2['GTI'])*100
dt2 = dt2.fillna(0)    
print(dt2)
dt2[['pitax', 'pitax_diff']].plot.bar()
plt.show()
"""







