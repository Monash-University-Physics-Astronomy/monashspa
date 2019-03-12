# Copyright 2019 School of Physics & Astronomy, Monash University
#
# This file is part of monashspa.
#
# monashspa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# monashspa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with monashspa.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np

from .testing_helpers import compare_dictionary

def test_basic_linear_fit():
    """Basic test of linear fit without uncertainties"""

    ### Get results ###
    from monashspa.common.fitting import linear_fit, get_fit_parameters

    data = [
        [1,	2.97958155926148, 0.435952175570949],
        [2,	4.84845692653319, 0.467234424802873],
        [3,	6.44561871392239, 0.740203944022575],
        [4,	8.72544337668039, 0.509084442407005],
        [5,	10.7326357174404, 0.557439432218125],
        [6,	12.3202409005262, 0.0236735417569119],
    ]
    data = np.array(data)

    fit_result = linear_fit(data[:,0], data[:,1])
    results = get_fit_parameters(fit_result)

    ### Expected results ###
    expected_results = {
        'slope': 1.903875935,
        'u_slope': 0.045590672,
        'intercept': 1.011763758,
        'u_intercept': 0.177550159,
    }
    precision = 1e-7

    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision)

    return success


def test_linear_fit_with_uncertainties():
    """Basic test of linear fit with uncertainties"""

    ### Get results ###
    from monashspa.common.fitting import linear_fit, get_fit_parameters

    data = [
        [1,	2.97958155926148, 0.435952175570949],
        [2,	4.84845692653319, 0.467234424802873],
        [3,	6.44561871392239, 0.740203944022575],
        [4,	8.72544337668039, 0.509084442407005],
        [5,	10.7326357174404, 0.557439432218125],
        [6,	12.3202409005262, 0.0236735417569119],
    ]
    data = np.array(data)

    fit_result = linear_fit(data[:,0], data[:,1], u_y=data[:,2])
    results = get_fit_parameters(fit_result)

    ### Expected results (from WFIT) ###
    expected_results = {
        'slope': 1.866046353,
        'u_slope': 0.064841588,
        'intercept': 1.124423955,
        'u_intercept': 0.387570521,
    }
    precision = 2e-8

    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision)

    return success

def test_failed_fit_1():
    """A test of the exception that should be raised if you don't use the independent variable"""
    ### Get results ###
    import monashspa.PHS2061 as spa
    from monashspa.common.fitting import MonashSPAFittingException

    # load the data
    data = spa.fitting_tutorial.data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model1 = spa.make_lmfit_model("A_0*exp(-l*x)")
    success = False
    try:
        model2 = spa.make_lmfit_model("A_0")
    except MonashSPAFittingException as e:
        if str(e).startswith('You have not used the independent variable'):
            success=True

    return success

def test_bypass_failed_fit_1():
    """A test of suppressing the exception that should be raised if you don't use the independent variable"""
    ### Get results ###
    import monashspa.PHS2061 as spa

    # load the data
    data = spa.fitting_tutorial.data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model1 = spa.make_lmfit_model("exp(-l*x)")
    model2 = spa.make_lmfit_model("A_0", allow_constant_model=True)
    model = model1*model2
    params = model.make_params(A_0=30, l=.005)
    params.add('halflife', expr="log(2)/l")
    fit_results = spa.model_fit(model, params, x=t, y=A, u_y=u_A)
    results = spa.get_fit_parameters(fit_results)
    
    ### Expected results ###
    expected_results = {
        'A_0': 20.573035990441486,
        'u_A_0': 0.6181473325960677,
        'l': 0.005004779941925933,
        'u_l': 0.00015840653659960648,
        'halflife': 138.49703455557113,
        'u_halflife': 4.38357646646529,
    }
    precision = 2e-7
    
    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision)

    return success

def test_failed_fit_2():
    """A test of not specifying a good initial guess for a parameter"""
    ### Get results ###
    import monashspa.PHS2061 as spa
    from monashspa.common.fitting import MonashSPAFittingException

    # load the data
    data = spa.fitting_tutorial.data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model = spa.make_lmfit_model("A_0*exp(-l*x)")
    params = model.make_params(A_0=30) # l will be "1" by default which is a bad guess
    params.add('halflife', expr="log(2)/l")
    success = False
    try:
        fit_results = spa.model_fit(model, params, x=t, y=A, u_y=u_A)
    except MonashSPAFittingException as e:
        if str(e).endswith('The fit failed. This is usually either because (a) you did not provide sufficient guesses for the model parameters, (b) you did not correctly specify the independent variable in your model (by default it must be "x"), or (c) the data you are fitting to contains NaN values.'):
            success=True
    
    return success

def do_tests():
    tests = [test_basic_linear_fit, test_linear_fit_with_uncertainties, test_failed_fit_1, test_bypass_failed_fit_1, test_failed_fit_2]
    failed_tests = []
    print('Running common fitting tests...')

    for testfn in tests:
        print('    Running test "{test_name}":'.format(test_name=testfn.__doc__))
        result = testfn()
        print('        Result: {result}'.format(result='success' if result else 'failure'))

        if not result:
            failed_tests.append(testfn)

    if failed_tests:
        print('')
        print('    There were {num_failures:d} failed common fitting tests'.format(num_failures=len(failed_tests)))
        
    print('')

    return failed_tests

if __name__ == "__main__":
    do_tests()