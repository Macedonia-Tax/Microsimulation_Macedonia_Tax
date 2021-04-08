"""
PIT (personal income tax) Calculator class.
"""
# CODING-STYLE CHECKS:
# pycodestyle calculator.py
# pylint --disable=locally-disabled calculator.py
#
# pylint: disable=too-many-lines
# pylintx: disable=no-value-for-parameter,too-many-lines

import os
import json
import re
import copy
import numpy as np
import pandas as pd
from taxcalc.functions import (cal_ssc_w, cal_tti_w, cal_pit_w, cal_net_i_w, cal_ssc_I, cal_tti_I, cal_pit_I, 
                               cal_net_i_I, cal_tti_c, cal_pit_c, cal_net_i_c, cal_total_gross_income, cal_total_taxable_income,
                               cal_total_pit)
from taxcalc.corpfunctions import (cit_liability)
from taxcalc.gstfunctions import (gst_liability)
from taxcalc.policy import Policy
from taxcalc.records import Records
from taxcalc.corprecords import CorpRecords
from taxcalc.gstrecords import GSTRecords
from taxcalc.utils import DIST_VARIABLES, create_distribution_table
# import pdb


class Calculator(object):
    """
    Constructor for the Calculator class.

    Parameters
    ----------
    policy: Policy class object
        this argument must be specified and object is copied for internal use

    records: Records class object
        this argument must be specified and object is copied for internal use

    corprecords: CorpRecords class object
        this argument must be specified and object is copied for internal use

    gstrecords: GSTRecords class object
        this argument must be specified and object is copied for internal use

    verbose: boolean
        specifies whether or not to write to stdout data-loaded and
        data-extrapolated progress reports; default value is true.

    sync_years: boolean
        specifies whether or not to synchronize policy year and records year;
        default value is true.

    Raises
    ------
    ValueError:
        if parameters are not the appropriate type.

    Returns
    -------
    class instance: Calculator

    Notes
    -----
    The most efficient way to specify current-law and reform Calculator
    objects is as follows:
         pol = Policy()
         rec = Records()
         grec = GSTRecords()
         crec = CorpRecords()
         # Current law
         calc1 = Calculator(policy=pol, records=rec, corprecords=crec,
                            gstrecords=grec)
         pol.implement_reform(...)
         # Reform
         calc2 = Calculator(policy=pol, records=rec, corprecords=crec,
                            gstrecords=grec)
    All calculations are done on the internal copies of the Policy and
    Records objects passed to each of the two Calculator constructors.
    """
    # pylint: disable=too-many-public-methods

    def __init__(self, policy=None, records=None, corprecords=None,
                 gstrecords=None, verbose=True, sync_years=True):
        # pylint: disable=too-many-arguments,too-many-branches
        if isinstance(policy, Policy):
            self.__policy = copy.deepcopy(policy)
        else:
            raise ValueError('must specify policy as a Policy object')
        if isinstance(records, Records):
            self.__records = copy.deepcopy(records)
        else:
            raise ValueError('must specify records as a Records object')
        if isinstance(gstrecords, GSTRecords):
            self.__gstrecords = copy.deepcopy(gstrecords)
        else:
            raise ValueError('must specify records as a GSTRecords object')
        if isinstance(corprecords, CorpRecords):
            self.__corprecords = copy.deepcopy(corprecords)
        else:
            raise ValueError('must specify records as a CorpRecords object')
        if self.__policy.current_year < self.__records.data_year:
            self.__policy.set_year(self.__records.data_year)
        current_year_is_data_year = (
            self.__records.current_year == self.__records.data_year)
        if sync_years and current_year_is_data_year:
            if verbose:
                print('You loaded data for ' +
                      str(self.__records.data_year) + '.')
                if self.__records.IGNORED_VARS:
                    print('Your data include the following unused ' +
                          'variables that will be ignored:')
                    for var in self.__records.IGNORED_VARS:
                        print('  ' +
                              var)
            while self.__records.current_year < self.__policy.current_year:
                self.__records.increment_year()
            if verbose:
                print('Tax-Calculator startup automatically ' +
                      'extrapolated your data to ' +
                      str(self.__records.current_year) + '.')
        assert self.__policy.current_year == self.__records.current_year
        assert self.__policy.current_year == self.__gstrecords.current_year
        assert self.__policy.current_year == self.__corprecords.current_year
        self.__stored_records = None

    def increment_year(self):
        """
        Advance all embedded objects to next year.
        """
        next_year = self.__policy.current_year + 1
        self.__records.increment_year()
        self.__gstrecords.increment_year()
        self.__corprecords.increment_year()
        self.__policy.set_year(next_year)

    def advance_to_year(self, year):
        """
        The advance_to_year function gives an optional way of implementing
        increment year functionality by immediately specifying the year
        as input.  New year must be at least the current year.
        """
        iteration = year - self.current_year
        if iteration < 0:
            raise ValueError('New current year must be ' +
                             'greater than current year!')
        for _ in range(iteration):
            self.increment_year()
        assert self.current_year == year

    def calc_all(self, zero_out_calc_vars=False):
        """
        Call all tax-calculation functions for the current_year.
        """
        # pylint: disable=too-many-function-args,no-value-for-parameter
        # conducts static analysis of Calculator object for current_year
        assert self.__records.current_year == self.__policy.current_year
        assert self.__gstrecords.current_year == self.__policy.current_year
        assert self.__corprecords.current_year == self.__policy.current_year
        self.__records.zero_out_changing_calculated_vars()
        # For now, don't zero out for corporate
        # pdb.set_trace()
        # Corporate calculations     
        cit_liability(self.__policy, self.__corprecords)
        
        # Individual calculations
        cal_ssc_w(self.__policy, self.__records)
        cal_tti_w(self.__policy, self.__records)
        cal_pit_w(self.__policy, self.__records)
        cal_net_i_w(self.__policy, self.__records)
        cal_ssc_I(self.__policy, self.__records)
        cal_tti_I(self.__policy, self.__records)
        cal_pit_I(self.__policy, self.__records)
        cal_net_i_I(self.__policy, self.__records)
        cal_tti_c(self.__policy, self.__records)
        cal_pit_c(self.__policy, self.__records)
        cal_net_i_c(self.__policy, self.__records)
        cal_total_gross_income(self.__policy, self.__records)
        cal_total_taxable_income(self.__policy, self.__records)
        cal_total_pit(self.__policy, self.__records)
        # GST calculations
        # agg_consumption(self.__policy, self.__gstrecords)
        # gst_liability_cereal(self.__policy, self.__gstrecords)
        # gst_liability_other(self.__policy, self.__gstrecords)
        gst_liability(self.__policy, self.__gstrecords)
        # TODO: ADD: expanded_income(self.__policy, self.__records)
        # TODO: ADD: aftertax_income(self.__policy, self.__records)

    def weighted_total(self, variable_name):
        """
        Return all-filing-unit weighted total of named Records variable.
        """
        return (self.array(variable_name) * self.array('weight')).sum()

    def weighted_garray(self, variable_name):
        """
        Return all-filing-unit weighted total of named Records variable.
        """
        return (self.garray(variable_name) * self.garray('weight'))

    def weighted_total_garray(self, variable_name):
        """
        Return all-filing-unit weighted total of named Records variable.
        """
        return (self.garray(variable_name) * self.garray('weight')).sum()

    def total_weight(self):
        """
        Return all-filing-unit total of sampling weights.
        NOTE: var_weighted_mean = calc.weighted_total(var)/calc.total_weight()
        """
        return self.array('weight').sum()

    def dataframe(self, variable_list):
        """
        Return pandas DataFrame containing the listed variables from embedded
        Records object.
        """
        assert isinstance(variable_list, list)
        arys = [self.array(vname) for vname in variable_list]
        pdf = pd.DataFrame(data=np.column_stack(arys), columns=variable_list)
        del arys
        return pdf

    def dataframe_cit(self, variable_list):
        """
        Return pandas DataFrame containing the listed variables from embedded
        CorpRecords object.
        """
        assert isinstance(variable_list, list)
        arys = [self.carray(vname) for vname in variable_list]
        pdf = pd.DataFrame(data=np.column_stack(arys), columns=variable_list)
        del arys
        return pdf
    
    def gini(self, variable):
        """
        Return pandas DataFrame containing the listed variables from embedded
        Records object.
        """
        assert isinstance(variable, list)
        variable = variable + ['weight']
        arys = [self.array(vname) for vname in variable]
        #print(arys)
        pdf = pd.DataFrame(data=np.column_stack(arys), columns=variable)
        del arys
        gini = pdf
        gini= gini.sort_values(by=variable)
        #gini['weight'] = 100
        gini['cumulative_weight']=np.cumsum(gini['weight'])
        sum_weight = (gini['weight']).sum()
        gini['percentage_cumul_pop'] = gini['cumulative_weight']/sum_weight
        gini['total_income'] = gini['weight']*gini[variable[0]]
        gini['cumulative_total_income']= np.cumsum(gini['total_income'])
        sum_total_income = sum(gini['total_income'])
        gini['percentage_cumul_income'] = gini['cumulative_total_income']/sum_total_income
        gini['height'] = gini['percentage_cumul_pop']-gini['percentage_cumul_income']
        gini1 = pd.DataFrame([[np.nan]*len(gini.columns)], columns=gini.columns)
        gini = gini1.append(gini, ignore_index=True)
        gini['percentage_cumul_pop']= gini['percentage_cumul_pop'].fillna(0)
        gini['percentage_cumul_income']= gini['percentage_cumul_income'].fillna(0)
        gini['height']= gini['height'].fillna(0)
        gini['base'] = gini.percentage_cumul_pop.diff()
        gini['base']= gini['base'].fillna(0)
        gini['integrate_area']= 0.5*gini['base']*(gini['height']+gini['height'].shift())
        sum_integrate_area = gini['integrate_area'].sum()
        gini_index = 2*(sum_integrate_area)
        
        #ploting gini coefficient
        import matplotlib.pyplot as plt
        
        n = 430
        w = np.exp(np.random.randn(n))
        
        f_vals = gini['percentage_cumul_pop']
        #f_vals = f_vals.append(pd.Series([1.0]))
        #print(f_vals)
        l_vals = gini['percentage_cumul_income']
        #l_vals = l_vals.append(pd.Series([1.0]))
        #print(l_vals)
        
        fig, ax = plt.subplots()
        ax.plot(f_vals, l_vals, label='Lorenz curve, lognormal sample')
        ax.plot(f_vals, f_vals, label='Line of Equality, 45 degrees')
        ax.legend()
        plt.show()
        return gini_index
    
    
    
    def distribution_table_dataframe(self):
        """
        Return pandas DataFrame containing the DIST_TABLE_COLUMNS variables
        from embedded Records object.
        """
        return self.dataframe(DIST_VARIABLES)

    def array(self, variable_name, variable_value=None):
        """
        If variable_value is None, return numpy ndarray containing the
         named variable in embedded Records object.
        If variable_value is not None, set named variable in embedded Records
         object to specified variable_value and return None (which can be
         ignored).
        """
        if variable_value is None:
            return getattr(self.__records, variable_name)
        assert isinstance(variable_value, np.ndarray)
        setattr(self.__records, variable_name, variable_value)
        return None

    def carray(self, variable_name, variable_value=None):
        """
        Corporate record version of array() function.
        If variable_value is None, return numpy ndarray containing the
         named variable in embedded Records object.
        If variable_value is not None, set named variable in embedded Records
         object to specified variable_value and return None (which can be
         ignored).
        """
        if variable_value is None:
            getattr(self.__corprecords, variable_name)
            return getattr(self.__corprecords, variable_name)
        assert isinstance(variable_value, np.ndarray)
        setattr(self.__corprecords, variable_name, variable_value)
        return None

    def garray(self, variable_name, variable_value=None):
        """
        GST record version of array() function.
        If variable_value is None, return numpy ndarray containing the
         named variable in embedded Records object.
        If variable_value is not None, set named variable in embedded Records
         object to specified variable_value and return None (which can be
         ignored).
        """
        if variable_value is None:
            return getattr(self.__gstrecords, variable_name)
        assert isinstance(variable_value, np.ndarray)
        setattr(self.__gstrecords, variable_name, variable_value)
        return None

    def n65(self):
        """
        Return numpy ndarray containing the number of
        individuals age 65+ in each filing unit.
        """
        vdf = self.dataframe(['age_head', 'age_spouse', 'elderly_dependents'])
        return ((vdf['age_head'] >= 65).astype(int) +
                (vdf['age_spouse'] >= 65).astype(int) +
                vdf['elderly_dependents'])

    def incarray(self, variable_name, variable_add):
        """
        Add variable_add to named variable in embedded Records object.
        """
        assert isinstance(variable_add, np.ndarray)
        setattr(self.__records, variable_name,
                self.array(variable_name) + variable_add)

    def zeroarray(self, variable_name):
        """
        Set named variable in embedded Records object to zeros.
        """
        setattr(self.__records, variable_name, np.zeros(self.array_len))

    def store_records(self):
        """
        Make internal copy of embedded Records object that can then be
        restored after interim calculations that make temporary changes
        to the embedded Records object.
        """
        assert self.__stored_records is None
        self.__stored_records = copy.deepcopy(self.__records)

    def restore_records(self):
        """
        Set the embedded Records object to the stored Records object
        that was saved in the last call to the store_records() method.
        """
        assert isinstance(self.__stored_records, Records)
        self.__records = copy.deepcopy(self.__stored_records)
        del self.__stored_records
        self.__stored_records = None

    def records_current_year(self, year=None):
        """
        If year is None, return current_year of embedded Records object.
        If year is not None, set embedded Records current_year to year and
         return None (which can be ignored).
        """
        if year is None:
            return self.__records.current_year
        assert isinstance(year, int)
        self.__records.set_current_year(year)
        return None

    @property
    def array_len(self):
        """
        Length of arrays in embedded Records object.
        """
        return self.__records.array_length

    def policy_param(self, param_name, param_value=None):
        """
        If param_value is None, return named parameter in
         embedded Policy object.
        If param_value is not None, set named parameter in
         embedded Policy object to specified param_value and
         return None (which can be ignored).
        """
        if param_value is None:
            return getattr(self.__policy, param_name)
        setattr(self.__policy, param_name, param_value)
        return None

    @property
    def reform_warnings(self):
        """
        Calculator class embedded Policy object's reform_warnings.
        """
        return self.__policy.parameter_warnings

    def policy_current_year(self, year=None):
        """
        If year is None, return current_year of embedded Policy object.
        If year is not None, set embedded Policy current_year to year and
         return None (which can be ignored).
        """
        if year is None:
            return self.__policy.current_year
        assert isinstance(year, int)
        self.__policy.set_year(year)
        return None

    @property
    def current_year(self):
        """
        Calculator class current assessment year property.
        """
        return self.__policy.current_year

    @property
    def data_year(self):
        """
        Calculator class initial (i.e., first) records data year property.
        """
        return self.__records.data_year

    def diagnostic_table(self, num_years):
        """
        Generate multi-year diagnostic table containing aggregate statistics;
        this method leaves the Calculator object unchanged.

        Parameters
        ----------
        num_years : Integer
            number of years to include in diagnostic table starting
            with the Calculator object's current_year (must be at least
            one and no more than what would exceed Policy end_year)

        Returns
        -------
        Pandas DataFrame object containing the multi-year diagnostic table
        """
        assert num_years >= 1
        max_num_years = self.__policy.end_year - self.__policy.current_year + 1
        assert num_years <= max_num_years
        diag_variables = DIST_VARIABLES + ['surtax']
        calc = copy.deepcopy(self)
        tlist = list()
        for iyr in range(1, num_years + 1):
            calc.calc_all()
            diag = create_diagnostic_table(calc.dataframe(diag_variables),
                                           calc.current_year)
            tlist.append(diag)
            if iyr < num_years:
                calc.increment_year()
        del diag_variables
        del calc
        del diag
        return pd.concat(tlist, axis=1)

    def distribution_tables(self, calc, groupby,
                            averages=False, scaling=True):
        """
        Get results from self and calc, sort them by GTI into table
        rows defined by groupby, compute grouped statistics, and
        return tables as a pair of Pandas dataframes.
        This method leaves the Calculator object(s) unchanged.
        Note that the returned tables have consistent income groups (based
        on the self GTI) even though the baseline GTI in self and
        the reform GTI in calc are different.

        Parameters
        ----------
        calc : Calculator object or None
            typically represents the reform while self represents the baseline;
            if calc is None, the second returned table is None

        groupby : String object
            options for input: 'weighted_deciles', 'standard_income_bins'
            determines how the columns in resulting Pandas DataFrame are sorted

        averages : boolean
            specifies whether or not monetary table entries are aggregates or
            averages (default value of False implies entries are aggregates)

        scaling : boolean
            specifies whether or not monetary table entries are scaled to
            billions and rounded to three decimal places when averages=False,
            or when averages=True, to thousands and rounded to three decimal
            places.  Regardless of the value of averages, non-monetary table
            entries are scaled to millions and rounded to three decimal places
            (default value of False implies entries are scaled and rounded)

        Return and typical usage
        ------------------------
        dist1, dist2 = calc1.distribution_tables(calc2, 'weighted_deciles')
        OR
        dist1, _ = calc1.distribution_tables(None, 'weighted_deciles')
        (where calc1 is a baseline Calculator object
        and calc2 is a reform Calculator object).
        Each of the dist1 and optional dist2 is a distribution table as a
        Pandas DataFrame with DIST_TABLE_COLUMNS and groupby rows.
        NOTE: when groupby is 'weighted_deciles', the returned tables have 3
              extra rows containing top-decile detail consisting of statistics
              for the 0.90-0.95 quantile range (bottom half of top decile),
              for the 0.95-0.99 quantile range, and
              for the 0.99-1.00 quantile range (top one percent); and the
              returned table splits the bottom decile into filing units with
              negative (denoted by a 0-10n row label),
              zero (denoted by a 0-10z row label), and
              positive (denoted by a 0-10p row label) values of the
              specified income_measure.
        """
        # nested function used only by this method
        def have_same_income_measure(calc1, calc2):
            """
            Return true if calc1 and calc2 contain the same GTI;
            otherwise, return false.  (Note that "same" means nobody's
            GTI differs by more than one cent.)
            """
            im1 = calc1.array('total_gross_income')
            im2 = calc2.array('total_gross_income')
            return np.allclose(im1, im2, rtol=0.0, atol=0.01)
        # main logic of method
        assert calc is None or isinstance(calc, Calculator)
        assert (groupby == 'weighted_deciles' or
                groupby == 'standard_income_bins')
        if calc is not None:
            assert np.allclose(self.array('weight'),
                               calc.array('weight'))  # rows in same order
        var_dataframe = self.distribution_table_dataframe()
        imeasure = 'total_gross_income'
        dt1 = create_distribution_table(var_dataframe, groupby, imeasure,
                                        averages, scaling)
        del var_dataframe
        if calc is None:
            dt2 = None
        else:
            assert calc.current_year == self.current_year
            assert calc.array_len == self.array_len
            var_dataframe = calc.distribution_table_dataframe()
            if have_same_income_measure(self, calc):
                imeasure = 'total_gross_income'
            else:
                imeasure = 'GTI_baseline'
                var_dataframe[imeasure] = self.array('total_gross_income')
            dt2 = create_distribution_table(var_dataframe, groupby, imeasure,
                                            averages, scaling)
            del var_dataframe
        return (dt1, dt2)

    def difference_table(self, calc, groupby, tax_to_diff):
        """
        Get results from self and calc, sort them by expanded_income into
        table rows defined by groupby, compute grouped statistics, and
        return tax-difference table as a Pandas dataframe.
        This method leaves the Calculator objects unchanged.
        Note that the returned tables have consistent income groups (based
        on the self expanded_income) even though the baseline expanded_income
        in self and the reform expanded_income in calc are different.

        Parameters
        ----------
        calc : Calculator object
            calc represents the reform while self represents the baseline

        groupby : String object
            options for input: 'weighted_deciles', 'standard_income_bins'
            determines how the columns in resulting Pandas DataFrame are sorted

        tax_to_diff : String object
            options for input: 'iitax', 'payrolltax', 'combined'
            specifies which tax to difference

        Returns and typical usage
        -------------------------
        diff = calc1.difference_table(calc2, 'weighted_deciles', 'iitax')
        (where calc1 is a baseline Calculator object
        and calc2 is a reform Calculator object).
        The returned diff is a difference table as a Pandas DataFrame
        with DIST_TABLE_COLUMNS and groupby rows.
        NOTE: when groupby is 'weighted_deciles', the returned table has three
              extra rows containing top-decile detail consisting of statistics
              for the 0.90-0.95 quantile range (bottom half of top decile),
              for the 0.95-0.99 quantile range, and
              for the 0.99-1.00 quantile range (top one percent); and the
              returned table splits the bottom decile into filing units with
              negative (denoted by a 0-10n row label),
              zero (denoted by a 0-10z row label), and
              positive (denoted by a 0-10p row label) values of the
              specified income_measure.
        """
        assert isinstance(calc, Calculator)
        assert calc.current_year == self.current_year
        assert calc.array_len == self.array_len
        self_var_dataframe = self.dataframe(DIFF_VARIABLES)
        calc_var_dataframe = calc.dataframe(DIFF_VARIABLES)
        diff = create_difference_table(self_var_dataframe,
                                       calc_var_dataframe,
                                       groupby, tax_to_diff)
        del self_var_dataframe
        del calc_var_dataframe
        return diff

    MTR_VALID_VARIABLES = [
        'SALARIES', 'INCOME_HP', 'PRFT_GAIN_BP_OTHR_SPECLTV_BUS',
        'PRFT_GAIN_BP_SPECLTV_BUS', 'PRFT_GAIN_BP_SPCFD_BUS',
        'PRFT_GAIN_BP_INC_115BBF', 'TOTAL_PROFTS_GAINS_BP', 'ST_CG_AMT_1',
        'ST_CG_AMT_2', 'ST_CG_AMT_APPRATE', 'TOTAL_SCTG', 'LT_CG_AMT_1',
        'LT_CG_AMT_2', 'TOTAL_LTCG', 'TOTAL_CAP_GAIN',
        'INCOME_OS_NOT_RACEHORSE', 'INC_CHARBLE_SPL_RATE',
        'INCOME_OS_RACEHORSE', 'TOTAL_INCOME_OS']

    def mtr(self, variable_str='SALARIES',
            negative_finite_diff=False,
            zero_out_calculated_vars=False,
            calc_all_already_called=False,
            wrt_full_compensation=True):
        """
        Calculates the marginal payroll, individual income, and combined
        tax rates for every tax filing unit, leaving the Calculator object
        in exactly the same state as it would be in after a calc_all() call.

        The marginal tax rates are approximated as the change in tax
        liability caused by a small increase (the finite_diff) in the variable
        specified by the variable_str divided by that small increase in the
        variable, when wrt_full_compensation is false.

        If wrt_full_compensation is true, then the marginal tax rates
        are computed as the change in tax liability divided by the change
        in total compensation caused by the small increase in the variable
        (where the change in total compensation is the sum of the small
        increase in the variable and any increase in the employer share of
        payroll taxes caused by the small increase in the variable).

        If using 'SALARIES' as variable_str, the marginal tax rate for all
        records where MARS != 2 will be missing.  If you want to perform a
        function such as np.mean() on the returned arrays, you will need to
        account for this.

        Parameters
        ----------
        variable_str: string
            specifies type of income or expense that is increased to compute
            the marginal tax rates.  See Notes for list of valid variables.

        negative_finite_diff: boolean
            specifies whether or not marginal tax rates are computed by
            subtracting (rather than adding) a small finite_diff amount
            to the specified variable.

        zero_out_calculated_vars: boolean
            specifies value of zero_out_calc_vars parameter used in calls
            of Calculator.calc_all() method.

        calc_all_already_called: boolean
            specifies whether self has already had its Calculor.calc_all()
            method called, in which case this method will not do a final
            calc_all() call but use the incoming embedded Records object
            as the outgoing Records object embedding in self.

        wrt_full_compensation: boolean
            specifies whether or not marginal tax rates on earned income
            are computed with respect to (wrt) changes in total compensation
            that includes the employer share of OASDI and HI payroll taxes.

        Returns
        -------
        A tuple of numpy arrays in the following order:
        mtr_payrolltax: an array of marginal payroll tax rates.
        mtr_incometax: an array of marginal individual income tax rates.
        mtr_combined: an array of marginal combined tax rates, which is
                      the sum of mtr_payrolltax and mtr_incometax.

        Notes
        -----
        The arguments zero_out_calculated_vars and calc_all_already_called
        cannot both be true.

        """
        # pylint: disable=too-many-arguments,too-many-statements
        # pylint: disable=too-many-locals,too-many-branches
        assert not zero_out_calculated_vars or not calc_all_already_called
        # check validity of variable_str parameter
        if variable_str not in Calculator.MTR_VALID_VARIABLES:
            msg = 'mtr variable_str="{}" is not valid'
            raise ValueError(msg.format(variable_str))
        # specify value for finite_diff parameter
        finite_diff = 1.0  # a one-rupee difference
        if negative_finite_diff:
            finite_diff *= -1.0
        # remember records object in order to restore it after mtr computations
        self.store_records()
        # extract variable array(s) from embedded records object
        variable = self.array(variable_str)
        if variable_str == 'SALARIES':
            earnings_var = self.array('SALARIES')
        elif variable_str == 'PRFT_GAIN_BP_OTHR_SPECLTV_BUS':
            seincome_var = self.array('PRFT_GAIN_BP_OTHR_SPECLTV_BUS')
        # calculate level of taxes after a marginal increase in income
        self.array(variable_str, variable + finite_diff)
        if variable_str == 'SALARIES':
            self.array('SALARIES', earnings_var + finite_diff)
        elif variable_str == 'SALARIES':
            self.array('SALARIES', earnings_var + finite_diff)
        elif variable_str == 'SALARIES':
            self.array('SALARIES', seincome_var + finite_diff)
        self.calc_all(zero_out_calc_vars=zero_out_calculated_vars)
        pitax_chng = self.array('pitax')
        # calculate base level of taxes after restoring records object
        self.restore_records()
        if not calc_all_already_called or zero_out_calculated_vars:
            self.calc_all(zero_out_calc_vars=zero_out_calculated_vars)
        pitax_base = self.array('pitax')
        # compute marginal changes in combined tax liability
        pitax_diff = pitax_chng - pitax_base
        # compute marginal tax rates
        mtr_pitax = pitax_diff / finite_diff
        # delete intermediate variables
        del variable
        if variable_str == 'SALARIES':
            del earnings_var
        elif variable_str == 'PRFT_GAIN_BP_OTHR_SPECLTV_BUS':
            del seincome_var
        del pitax_chng
        del pitax_base
        del pitax_diff
        # return the marginal tax rate array
        return mtr_pitax

    REQUIRED_REFORM_KEYS = set(['policy'])
    # THE REQUIRED_ASSUMP_KEYS ARE OBSOLETE BECAUSE NO ASSUMP FILES ARE USED
    REQUIRED_ASSUMP_KEYS = set(['consumption', 'behavior',
                                'growdiff_baseline', 'growdiff_response',
                                'growmodel'])

    @staticmethod
    def read_json_param_objects(reform, assump):
        """
        Read JSON reform object [and formerly assump object] and
        return a single dictionary containing 6 key:dict pairs:
        'policy':dict, 'consumption':dict, 'behavior':dict,
        'growdiff_baseline':dict, 'growdiff_response':dict, and
        'growmodel':dict.

        Note that either of the two function arguments can be None.
        If reform is None, the dict in the 'policy':dict pair is empty.
        If assump is None, the dict in the all the key:dict pairs is empty.

        Also note that either of the two function arguments can be strings
        containing a valid JSON string (rather than a filename),
        in which case the file reading is skipped and the appropriate
        read_json_*_text method is called.

        The reform file contents or JSON string must be like this:
        {"policy": {...}}
        and the assump file contents or JSON string must be like this:
        {"consumption": {...},
         "behavior": {...},
         "growdiff_baseline": {...},
         "growdiff_response": {...},
         "growmodel": {...}}
        The {...} should be empty like this {} if not specifying a policy
        reform or if not specifying any economic assumptions of that type.

        The returned dictionary contains parameter lists (not arrays).
        """
        # pylint: disable=too-many-branches
        # first process second assump parameter
        assert assump is None
        if assump is None:
            cons_dict = dict()
            behv_dict = dict()
            gdiff_base_dict = dict()
            gdiff_resp_dict = dict()
            growmodel_dict = dict()
        elif isinstance(assump, str):
            if os.path.isfile(assump):
                txt = open(assump, 'r').read()
            else:
                txt = assump
            (cons_dict,
             behv_dict,
             gdiff_base_dict,
             gdiff_resp_dict,
             growmodel_dict) = Calculator._read_json_econ_assump_text(txt)
        else:
            raise ValueError('assump is neither None nor string')
        # next process first reform parameter
        if reform is None:
            rpol_dict = dict()
        elif isinstance(reform, str):
            if os.path.isfile(reform):
                txt = open(reform, 'r').read()
            else:
                txt = reform
            rpol_dict = Calculator._read_json_policy_reform_text(txt)
        else:
            raise ValueError('reform is neither None nor string')
        # construct single composite dictionary
        param_dict = dict()
        param_dict['policy'] = rpol_dict
        param_dict['consumption'] = cons_dict
        param_dict['behavior'] = behv_dict
        param_dict['growdiff_baseline'] = gdiff_base_dict
        param_dict['growdiff_response'] = gdiff_resp_dict
        param_dict['growmodel'] = growmodel_dict
        # return the composite dictionary
        return param_dict

    @staticmethod
    def reform_documentation(params, policy_dicts=None):
        """
        Generate reform documentation.

        Parameters
        ----------
        params: dict
            dictionary is structured like dict returned from
            the static Calculator method read_json_param_objects()

        policy_dicts : list of dict or None
            each dictionary in list is a params['policy'] dictionary
            representing second and subsequent elements of a compound
            reform; None implies no compound reform with the simple
            reform characterized in the params['policy'] dictionary

        Returns
        -------
        doc: String
            the documentation for the policy reform specified in params
        """
        # pylint: disable=too-many-statements,too-many-branches

        # nested function used only in reform_documentation
        def param_doc(years, change, base):
            """
            Parameters
            ----------
            years: list of change years
            change: dictionary of parameter changes
            base: Policy object with baseline values
            syear: parameter start assessment year

            Returns
            -------
            doc: String
            """
            # pylint: disable=too-many-locals

            # nested function used only in param_doc
            def lines(text, num_indent_spaces, max_line_length=77):
                """
                Return list of text lines, each one of which is no longer
                than max_line_length, with the second and subsequent lines
                being indented by the number of specified num_indent_spaces;
                each line in the list ends with the '\n' character
                """
                if len(text) < max_line_length:
                    # all text fits on one line
                    line = text + '\n'
                    return [line]
                # all text does not fix on one line
                first_line = True
                line_list = list()
                words = text.split()
                while words:
                    if first_line:
                        line = ''
                        first_line = False
                    else:
                        line = ' ' * num_indent_spaces
                    while (words and
                           (len(words[0]) + len(line)) < max_line_length):
                        line += words.pop(0) + ' '
                    line = line[:-1] + '\n'
                    line_list.append(line)
                return line_list

            # begin main logic of param_doc
            # pylint: disable=too-many-nested-blocks
            assert len(years) == len(change.keys())
            assert isinstance(base, Policy)
            basex = copy.deepcopy(base)
            basevals = getattr(basex, '_vals', None)
            assert isinstance(basevals, dict)
            doc = ''
            for year in years:
                # write year
                basex.set_year(year)
                doc += '{}:\n'.format(year)
                # write info for each param in year
                for param in sorted(change[year].keys()):
                    # ... write param:value line
                    pval = change[year][param]
                    if isinstance(pval, list):
                        pval = pval[0]
                        if basevals[param]['boolean_value']:
                            if isinstance(pval, list):
                                pval = [True if item else
                                        False for item in pval]
                            else:
                                pval = bool(pval)
                    doc += ' {} : {}\n'.format(param, pval)
                    # ... write optional param-index line
                    if isinstance(pval, list):
                        pval = basevals[param]['col_label']
                        pval = [str(item) for item in pval]
                        doc += ' ' * (4 + len(param)) + '{}\n'.format(pval)
                    # ... write name line
                    if param.endswith('_cpi'):
                        rootparam = param[:-4]
                        name = '{} inflation indexing status'.format(rootparam)
                    else:
                        name = basevals[param]['long_name']
                    for line in lines('name: ' + name, 6):
                        doc += '  ' + line
                    # ... write optional desc line
                    if not param.endswith('_cpi'):
                        desc = basevals[param]['description']
                        for line in lines('desc: ' + desc, 6):
                            doc += '  ' + line
                    # ... write baseline_value line
                    if param.endswith('_cpi'):
                        rootparam = param[:-4]
                        bval = basevals[rootparam].get('cpi_inflated',
                                                       False)
                    else:
                        bval = getattr(basex, param[1:], None)
                        if isinstance(bval, np.ndarray):
                            bval = bval.tolist()
                            if basevals[param]['boolean_value']:
                                bval = [True if item else
                                        False for item in bval]
                        elif basevals[param]['boolean_value']:
                            bval = bool(bval)
                    doc += '  baseline_value: {}\n'.format(bval)
            return doc

        # begin main logic of reform_documentation
        # create Policy object with pre-reform (i.e., baseline) values
        clp = Policy()
        # generate documentation text
        doc = 'REFORM DOCUMENTATION\n'
        doc += 'Policy Reform Parameter Values by Year:\n'
        years = sorted(params['policy'].keys())
        if years:
            doc += param_doc(years, params['policy'], clp)
        else:
            doc += 'none: using current-law policy parameters\n'
        if policy_dicts is not None:
            assert isinstance(policy_dicts, list)
            base = clp
            base.implement_reform(params['policy'])
            assert not base.parameter_errors
            for policy_dict in policy_dicts:
                assert isinstance(policy_dict, dict)
                doc += 'Policy Reform Parameter Values by Year:\n'
                years = sorted(policy_dict.keys())
                doc += param_doc(years, policy_dict, base)
                base.implement_reform(policy_dict)
                assert not base.parameter_errors
        return doc

    # ----- begin private methods of Calculator class -----

    @staticmethod
    def _read_json_policy_reform_text(text_string):
        """
        Strip //-comments from text_string and return 1 dict based on the JSON.

        Specified text is JSON with at least 1 high-level key:object pair:
        a "policy": {...} pair.  Other keys will raise a ValueError.

        The {...}  object may be empty (that is, be {}), or
        may contain one or more pairs with parameter string primary keys
        and string years as secondary keys.  See tests/test_calculator.py for
        an extended example of a commented JSON policy reform text
        that can be read by this method.

        Returned dictionary prdict has integer years as primary keys and
        string parameters as secondary keys.  This returned dictionary is
        suitable as the argument to the Policy implement_reform(prdict) method.
        """
        # pylint: disable=too-many-locals
        # strip out //-comments without changing line numbers
        json_str = re.sub('//.*', ' ', text_string)
        # convert JSON text into a Python dictionary
        try:
            raw_dict = json.loads(json_str)
        except ValueError as valerr:
            msg = 'Policy reform text below contains invalid JSON:\n'
            msg += str(valerr) + '\n'
            msg += 'Above location of the first error may be approximate.\n'
            msg += 'The invalid JSON reform text is between the lines:\n'
            bline = 'XX----.----1----.----2----.----3----.----4'
            bline += '----.----5----.----6----.----7'
            msg += bline + '\n'
            linenum = 0
            for line in json_str.split('\n'):
                linenum += 1
                msg += '{:02d}{}'.format(linenum, line) + '\n'
            msg += bline + '\n'
            raise ValueError(msg)
        # check key contents of dictionary
        actual_keys = set(raw_dict.keys())
        missing_keys = Calculator.REQUIRED_REFORM_KEYS - actual_keys
        if missing_keys:
            msg = 'required key(s) "{}" missing from policy reform file'
            raise ValueError(msg.format(missing_keys))
        illegal_keys = actual_keys - Calculator.REQUIRED_REFORM_KEYS
        if illegal_keys:
            msg = 'illegal key(s) "{}" in policy reform file'
            raise ValueError(msg.format(illegal_keys))
        # convert raw_dict['policy'] dictionary into prdict
        raw_dict_policy = raw_dict['policy']
        tdict = Policy.translate_json_reform_suffixes(raw_dict['policy'])
        prdict = Calculator._convert_parameter_dict(tdict)
        return prdict

    @staticmethod
    def _read_json_econ_assump_text(text_string):
        """
        Strip //-comments from text_string and return 5 dict based on the JSON.
        Specified text is JSON with at least 5 high-level key:value pairs:
        a "consumption": {...} pair,
        a "behavior": {...} pair,
        a "growdiff_baseline": {...} pair,
        a "growdiff_response": {...} pair, and
        a "growmodel": {...} pair.
        Other keys such as "policy" will raise a ValueError.
        The {...}  object may be empty (that is, be {}), or
        may contain one or more pairs with parameter string primary keys
        and string years as secondary keys.  See tests/test_calculator.py for
        an extended example of a commented JSON economic assumption text
        that can be read by this method.
        Note that an example is shown in the ASSUMP_CONTENTS string in
        the tests/test_calculator.py file.
        Returned dictionaries (cons_dict, behv_dict, gdiff_baseline_dict,
        gdiff_respose_dict, growmodel_dict) have integer years as primary
        keys and string parameters as secondary keys.
        These returned dictionaries are suitable as the arguments to
        the Consumption.update_consumption(cons_dict) method, or
        the Behavior.update_behavior(behv_dict) method, or
        the GrowDiff.update_growdiff(gdiff_dict) method, or
        the GrowModel.update_growmodel(growmodel_dict) method.
        """
        # pylint: disable=too-many-locals
        # strip out //-comments without changing line numbers
        json_str = re.sub('//.*', ' ', text_string)
        # convert JSON text into a Python dictionary
        try:
            raw_dict = json.loads(json_str)
        except ValueError as valerr:
            msg = 'Economic assumption text below contains invalid JSON:\n'
            msg += str(valerr) + '\n'
            msg += 'Above location of the first error may be approximate.\n'
            msg += 'The invalid JSON asssump text is between the lines:\n'
            bline = 'XX----.----1----.----2----.----3----.----4'
            bline += '----.----5----.----6----.----7'
            msg += bline + '\n'
            linenum = 0
            for line in json_str.split('\n'):
                linenum += 1
                msg += '{:02d}{}'.format(linenum, line) + '\n'
            msg += bline + '\n'
            raise ValueError(msg)
        # check key contents of dictionary
        actual_keys = set(raw_dict.keys())
        missing_keys = Calculator.REQUIRED_ASSUMP_KEYS - actual_keys
        if missing_keys:
            msg = 'required key(s) "{}" missing from economic assumption file'
            raise ValueError(msg.format(missing_keys))
        illegal_keys = actual_keys - Calculator.REQUIRED_ASSUMP_KEYS
        if illegal_keys:
            msg = 'illegal key(s) "{}" in economic assumption file'
            raise ValueError(msg.format(illegal_keys))
        # convert the assumption dictionaries in raw_dict
        key = 'consumption'
        cons_dict = Calculator._convert_parameter_dict(raw_dict[key])
        key = 'behavior'
        behv_dict = Calculator._convert_parameter_dict(raw_dict[key])
        key = 'growdiff_baseline'
        gdiff_base_dict = Calculator._convert_parameter_dict(raw_dict[key])
        key = 'growdiff_response'
        gdiff_resp_dict = Calculator._convert_parameter_dict(raw_dict[key])
        key = 'growmodel'
        growmodel_dict = Calculator._convert_parameter_dict(raw_dict[key])
        return (cons_dict, behv_dict, gdiff_base_dict, gdiff_resp_dict,
                growmodel_dict)

    @staticmethod
    def _convert_parameter_dict(param_key_dict):
        """
        Converts specified param_key_dict into a dictionary whose primary
        keys are assessment years, and hence, is suitable as the argument
        to the Policy.implement_reform() method.

        Specified input dictionary has string parameter primary keys and
        string years as secondary keys.

        Returned dictionary has integer years as primary keys and
        string parameters as secondary keys.
        """
        # convert year skey strings into integers and
        # optionally convert lists into np.arrays
        year_param = dict()
        for pkey, sdict in param_key_dict.items():
            if not isinstance(pkey, str):
                msg = 'pkey {} in reform is not a string'
                raise ValueError(msg.format(pkey))
            rdict = dict()
            if not isinstance(sdict, dict):
                msg = 'pkey {} in reform is not paired with a dict'
                raise ValueError(msg.format(pkey))
            for skey, val in sdict.items():
                if not isinstance(skey, str):
                    msg = 'skey {} in reform is not a string'
                    raise ValueError(msg.format(skey))
                else:
                    year = int(skey)
                rdict[year] = val
            year_param[pkey] = rdict
        # convert year_param dictionary to year_key_dict dictionary
        year_key_dict = dict()
        years = set()
        for param, sdict in year_param.items():
            for year, val in sdict.items():
                if year not in years:
                    years.add(year)
                    year_key_dict[year] = dict()
                year_key_dict[year][param] = val
        return year_key_dict
