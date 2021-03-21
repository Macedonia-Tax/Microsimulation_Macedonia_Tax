"""
app1.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app1.py > app1.res
CHECK: Use your favorite Windows diff utility to confirm that app1.res is
       the same as the app1.out file that is in the repository.
"""
from taxcalc import*
import matplotlib.pyplot as plt
import pandas as pd 

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
year = 2019


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

dump_vars = ['id_n','total_gross_income','total_taxable_income', 'ssc_w', 'total_pit']
dumpdf = calc1.dataframe(dump_vars)
column_order = dumpdf.columns

assert len(dumpdf.index) == calc1.array_len

dumpdf.to_csv('app0-dump_macedonia.csv', columns=column_order,
              index=False, float_format='%.0f')

#output_categories = 'standard_income_bins'
output_categories = 'weighted_deciles'
output_in_averages = False

dt1, dt2 = calc1.distribution_tables(calc2, output_categories,
                                     averages=output_in_averages,
                                     scaling=True)

dt2['pitax_diff'] = dt2['total_pit'] - dt1['total_pit']

dt1 = dt1.fillna(0)
dt2 = dt2.fillna(0)
if output_in_averages:
    print('***************************  Average Tax Burden ', end=' ')
    print(f'(in MKD.) per Taxpayer for {year}  ***************************')
    pd.options.display.float_format = '{:.0f}'.format
else:
    print('*****************  Distribution Tables ', end=' ')
    print(f'for Total Tax Collection (in MKD millions) for {year} *********')
    #pd.options.display.float_format = '{:,.0f}'.format
    pd.options.display.float_format = '{:.0f}'.format
                
print('\n')
print('  *** CURRENT-LAW DISTRIBUTION TABLE ***')
#print('\n')
print(dt1)
print('\n')
print('  *** POLICY-REFORM DISTRIBUTION TABLE ***')
#print('\n')
print(dt2)
print('\n')


dt1.columns
"""chart"""
ax = dt1[:-1].plot(kind='bar', use_index=True, y='total_pit',
legend=False, rot=90,
figsize=(8,8))
ax.set_ylabel('PIT in mkd')
ax.set_xlabel('GTI bins')
ax.set_title(' PIT Distribution Under Current Law (2019)', fontweight="bold")
#pic_filename1 = 'CIT Collection 2017.png'
#plt.savefig(pic_filename1)
plt.plot

dt2.columns
"""chart2"""
ay = dt2[:-1].plot(kind='bar', use_index=True, y='total_pit',
legend=False, rot=90,
figsize=(8,8))
ax.set_ylabel('PIT in mkd')
ax.set_xlabel('GTI bins')
ax.set_title(' PIT Distribution Under Reform', fontweight="bold")
#pic_filename1 = 'CIT Collection 2017.png'
#plt.savefig(pic_filename1)
plt.plot



