"""
app02.py illustrates use of TPRU-India taxcalc release 2.0.0
USAGE: python app02.py > app02.res
CHECK: Use your favorite Windows diff utility to confirm that app02.res is
       the same as the app02.out file that is in the repository.
"""
import pandas as pd
from taxcalc import *

# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

grecs = GSTRecords()

# create CorpRecords object using cross-section data
crecs1 = CorpRecords(data='cit_cross.csv', weights='cit_cross_wgts.csv')

# create CorpRecords object using panel data
crecs2 = CorpRecords(data='cit_panel.csv', data_type='panel')

# create Policy object containing current-law polic
pol1 = Policy()
pol2 = Policy()
reform = Calculator.read_json_param_objects('app01_reform.json', None)
pol2.implement_reform(reform['policy'])

# specify Calculator objects for current-law policy
calc1c = Calculator(policy=pol1, records=recs, corprecords=crecs1,
                    gstrecords=grecs, verbose=False)
calc1p = Calculator(policy=pol1, records=recs, corprecords=crecs2,
                    gstrecords=grecs, verbose=False)
calc2c = Calculator(policy=pol2, records=recs, corprecords=crecs1,
                    gstrecords=grecs, verbose=False)
calc2p = Calculator(policy=pol2, records=recs, corprecords=crecs2,
                    gstrecords=grecs, verbose=False)

print(f'**Cross-Section Data**')
for year in range(2017, 2022):
    calc1c.advance_to_year(year)
    calc1p.advance_to_year(year)
    calc2c.advance_to_year(year)
    calc2p.advance_to_year(year)
    # Produce DataFrame of results using cross-section
    calc1c.calc_all()
    AggIncCB = calc1c.carray('GTI_Before_Loss')
    GTICB = calc1c.carray('GTI')
    TTICB = calc1c.carray('TTI')
    citaxCB = calc1c.carray('citax')
    citax_MATCB = calc1c.carray('citax_after_MAT')    
    wgtCB = calc1c.carray('weight')
    etrCB = np.divide(citax_MATCB,AggIncCB)
    etrCB[~np.isfinite(etrCB)] = 0
    wtd_etrCB = sum(etrCB*wgtCB.values/sum(wgtCB.values))

    calc2c.calc_all()
    AggIncCR = calc2c.carray('GTI_Before_Loss')
    GTICR = calc2c.carray('GTI')
    TTICR = calc2c.carray('TTI')
    citaxCR = calc2c.carray('citax')
    citax_MATCR = calc2c.carray('citax_after_MAT')    
    wgtCR = calc2c.carray('weight')
    etrCR = np.divide(citax_MATCR,AggIncCR)
    etrCR[~np.isfinite(etrCR)] = 0
    wtd_etrCR = sum(etrCR*wgtCR.values/sum(wgtCR.values))   

    # Produce DataFrame of results using panel
    calc1p.calc_all()
    AggIncPB = calc1p.carray('GTI_Before_Loss')
    GTIPB = calc1p.carray('GTI')
    TTIPB = calc1p.carray('TTI')
    citaxPB = calc1p.carray('citax')
    wgtPB = calc1p.carray('weight')

    calc2p.calc_all()
    AggIncPR = calc2p.carray('GTI_Before_Loss')
    GTIPR = calc2p.carray('GTI')
    TTIPR = calc2p.carray('TTI')
    citaxPR = calc2p.carray('citax')
    wgtPR = calc2p.carray('weight')

    # print(f'Year  {year}: {weighted_tax1 * 1e-9:,.2f}')
    print(f'************* Year  {year}  *************')
    # print('*************Year  ' + str(year) + '   *************')
    print('\n')
    print(f'**Baseline**')
    print('\n')
    print(f'GTI before loss, : {sum(AggIncCB * wgtCB) / 10**9:,.0f} Billion')
    print(f'GTI, : {sum(GTICB * wgtCB) / 10**9:,.0f} Billion')
    print(f'TTI, : {sum(TTICB * wgtCB) / 10**9:,.0f} Billion')
    print(f'Tax, : {sum(citaxCB * wgtCB) / 10**9:,.0f} Billion')
    print(f'Tax with MAT, : {sum(citax_MATCB * wgtCB) / 10**9:,.0f} Billion')
    print(f'Effective Tax Rate, : {wtd_etrCB*100:,.1f}%')
    print('\n')
    print(f'**Reform**')
    print('\n')
    print(f'GTI before loss, : {sum(AggIncCR * wgtCR) / 10**9:,.0f} Billion')
    print(f'GTI, : {sum(GTICR * wgtCR) / 10**9:,.0f} Billion')
    print(f'TTI, : {sum(TTICB * wgtCB) / 10**9:,.0f} Billion')
    print(f'Tax, : {sum(citaxCR * wgtCR) / 10**9:,.0f} Billion')
    print(f'Tax with MAT, : {sum(citax_MATCR * wgtCR) / 10**9:,.0f} Billion')
    print(f'Effective Tax Rate, : {wtd_etrCR*100:,.1f}%')   

    print('\n')    
    print(f'Change in Tax Collection, : {sum((citaxCR - citaxCB) * wgtCB) / 10**9:,.0f} Billion')
    print('\n')



'''
    print('GTI before loss, baseline, panel: ' +
          str(sum(AggIncPB * wgtPB) / 10**7))
    print('GTI, baseline, panel: ' + str(sum(GTIPB * wgtPB) / 10**7))
    print('TTI, baseline, panel: ' + str(sum(TTIPB * wgtPB) / 10**7))
    print('Tax, baseline, panel: ' + str(sum(citaxPB * wgtPB) / 10**7))
    print('\n')
    print('GTI before loss, reform, panel: ' +
          str(sum(AggIncPR * wgtPR) / 10**7))
    print('GTI, reform, panel: ' + str(sum(GTIPR * wgtPR) / 10**7))
    print('TTI, reform, panel: ' + str(sum(TTIPR * wgtPR) / 10**7))
    print('Tax, reform, panel: ' + str(sum(citaxPR * wgtPR) / 10**7))
    print('\n')
    print('Change in tax, panel: ' +
          str(sum((citaxPR - citaxPB) * wgtPB) / 10**7))
    print('\n')
'''