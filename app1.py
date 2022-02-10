"""
app1.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app1.py > app1.res
CHECK: Use your favorite Windows diff utility to confirm that app1.res is
       the same as the app1.out file that is in the repository.
"""
from taxcalc import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

"""
dump_vars = ['id_n','total_gross_income','total_taxable_income','total_pit','total_n_icome']
dumpdf = calc1.dataframe(dump_vars)
dumpdf= dumpdf.sort_values(by=['total_gross_income'])
dumpdf.to_csv('app1-dump_macedonia.csv',
              index=False, float_format='%.0f')
"""
#Thi below gini shows the income distribution for the population that pays taxes
#gini_vars = ['total_gross_income','total_n_icome','total_n_icome']
#dumpdf = calc1.dataframe(gini_vars)

#gini_pre_tax = calc1.gini(dumpdf[['total_gross_income', 'total_n_icome']])
#print(gini_pre_tax)
gini_pre_tax = calc1.gini(['total_gross_income'])
print(gini_pre_tax)

gini_post_tax = calc1.gini(['total_n_icome'])
print(gini_post_tax)

gini_post_tax_reform = calc2.gini(['total_n_icome'])
print(gini_post_tax_reform)

#in place of before tax income
gini_gross_salaries = calc1.gini(['gross_i_w'])
print(gini_gross_salaries)

#Kakwani index of progressivity K(P)
"""
Fig. 2. Computation of the Kakwani’s Index of Inequality – K(I). Kakwani’s Index K(I) = 2 × (Area bounded by the Before-Tax and After-Tax Income curves)
"""
Area_under_Before_Tax_Income_curve = gini_pre_tax
Area_under_After_Tax_Income_curve = gini_post_tax
ki = 2*(gini_post_tax-gini_pre_tax)
print(f'KI Index is {ki}')
#ki_curve = calc1.gini(['ki'])
#K(I) = Ginibefore-tax income − Giniafter-tax income
#For a proportional tax, K(P) will be zero and for a progressive tax, K(P) will be positive.10 Larger values of K(P) indicate greater progressivity

    
#Share of Income tax burden by age    
#Share of Income tax burden by gender 
#group by age, number of tax returns, tax liability,
dump_vars = ['y_b', 'total_gross_income', 'total_taxable_income','total_n_icome','total_pit']
df = calc1.dataframe(dump_vars)
df.rename(columns = {'y_b':'age'}, inplace = True)
bins = pd.cut(df['age'], [0, 18, 25, 35, 45, 55, 65, 100], labels=('under 18', '18 under 25', '25 under 35', '35 under 45', '45 under 55', '55 under 65', '65 and over'))
df_age = df.groupby(bins)['total_gross_income','total_taxable_income','total_n_icome','total_pit'].sum()
df_age_mm = (df_age/10**6).reset_index()
print(df_age_mm)


dump_vars1 = ['gender', 'total_gross_income', 'total_taxable_income','total_n_icome','total_pit']
df1 = calc1.dataframe(dump_vars1)
df1['gender'].replace([0,1],['Female','Male'],inplace=True)
df1
df1_gender = df1.groupby(by = 'gender')['total_gross_income','total_taxable_income','total_n_icome','total_pit'].sum()
df1_gender_mm = (df1_gender/10**6).reset_index()
print(df1_gender_mm)

"""
plt.bar(df_age)
plt.title('Tax Liability by Age Group')
plt.xlabel('Age_Groups')
plt.ylabel('Liability')
plt.show()
"""


#df = df_age.groupby(['y_b']).sum()
#df_age['Age Groups'] = pd.qcut(df_age['y_b'], [0, 18, 25, 35, 45, 55, 65, 100], labels=['under 18', '18 under 25', '25 under 35', '35 under 45', '45 under 55', '55 under 65', '65 and over'])
#print(df_age.head())
# her we define the threshhold or our age groups
#age_groups = [0, 18, 25, 35, 45, 55, 65, 100]
# and for convenience we give each of them a handy label
#age_group_names = ['under 18', '18 under 25', '25 under 35', '35 under 45', '45 under 55', '55 under 65', '65 and over']
#dumpdf_2019['Age group'] = calc1.dataframe(dumpdf_2019['y_b'], bins=age_groups, labels=age_group_names)
#dumpdf_2019.head()
#df = dumpdf.groupby(['gender',bins]).sum()
#df.head(1)


"""
import inequalipy as ineq
import numpy as np
from inequalipy import *
atkinson.index(a)
a= np.random.normal(5,1,100)
weight = np.ones(len(a), dtype=int)


ede_pre_tax = calc1.ede(['total_gross_income'])
print(ede_pre_tax)

ede_post_tax = calc1.ede(['total_n_icome'])
print(ede_pre_tax)

ede_post_tax_reform = calc2.ede(['total_n_icome'])
print(ede_pre_tax)
 


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






