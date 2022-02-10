"""
app2.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app2.py
"""
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Records object containing pit.csv and pit_weights.csv input data
grecs = GSTRecords()

# create CorpRecords object containing cit.csv and cit_weights.csv input data
crecs = CorpRecords()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app1_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, gstrecords=grecs,
                   corprecords=crecs, verbose=False)

# Loop through years 2019, 2020 and 2021 and print out pitax
for year in range(2019,2024):
    calc1.advance_to_year(year)
    calc2.advance_to_year(year)
    calc1.calc_all()
    calc2.calc_all()
    weighted_tax1 = calc1.weighted_total('total_pit')
    weighted_tax2 = calc2.weighted_total('total_pit')
    total_weights = calc1.total_weight()

    print(f'Tax under current law for {year}: {weighted_tax1 * 1e-9:,.2f} billions')
    print(f'Tax under reform for {year}: {weighted_tax2 * 1e-9:,.2f} billions')
    print(f'Total number of tax returns for {year}: {total_weights * 1e-3:,.2f} thousands')

    
    
    


