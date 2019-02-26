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

from ..testing_helpers import compare_dictionary

def nonlinear_fit():
    """Basic test of PHS2061 nonlinear fit"""

    ### Get results ###
    import monashspa.PHS2061 as spa

    # load the data
    data = spa.fitting_tutorial.data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model = spa.make_lmfit_model("A_0*exp(-l*x)")
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

def nonlinear_fit_with_independent_as_t():
    """Test of PHS2061 nonlinear fit using an independent variable that was not 'x'"""

    ### Get results ###
    import monashspa.PHS2061 as spa

    # load the data
    data = spa.fitting_tutorial.data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model = spa.make_lmfit_model("A_0*exp(-l*t)", independent_vars=["t"])
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

def linear_fit_model():
    """Test of PHS2061 linear fit using custom model"""

    ### Get results ###
    import monashspa.PHS2061 as spa

    # load the data
    data = spa.fitting_tutorial.data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model = spa.make_lmfit_model("m*x+c")
    params = model.make_params(m=0.04, c=5)
    params.add('halflife', expr="-log(2)/m")
    params.add('A_0', expr="exp(c)")
    fit_results = spa.model_fit(model, params, x=t, y=np.log(A), u_y=u_A/A)
    results = spa.get_fit_parameters(fit_results)

    ### Expected results ###
    expected_results = {
        'c': 3.02843895796932,
        'u_c': 0.030620495054301592,
        'm': -0.004897938859868103,
        'u_m': 0.0001633020007207088,
        'halflife': 141.51813658584769,
        'u_halflife': 4.718351025589936,
        'A_0': 20.664948544330286,
        'u_A_0': 0.6327709546990624,
    }
    precision = 1e-5

    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision)

    return success

def linear_fit():
    """Basic test of PHS2061 linear fit"""

    ### Get results ###
    import monashspa.PHS2061 as spa

    # load the data
    data = spa.fitting_tutorial.data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    fit_results = spa.linear_fit(t, np.log(A), u_y=u_A/A)
    results = spa.get_fit_parameters(fit_results)

    ### Expected results ###
    expected_results = {
        'intercept': 3.02843895796932,
        'u_intercept': 0.030620495054301592,
        'slope': -0.004897938859868103,
        'u_slope': 0.0001633020007207088,
    }
    precision = 1e-7

    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision)

    return success

def do_tests():
    tests = [nonlinear_fit, nonlinear_fit_with_independent_as_t, linear_fit, linear_fit_model]
    failed_tests = []

    print('Running PHS2061 fitting tutorial tests...')

    for testfn in tests:
        print('    Running test "{test_name}":'.format(test_name=testfn.__doc__))
        result = testfn()
        print('        Result: {result}'.format(result='success' if result else 'failure'))

        if not result:
            failed_tests.append(testfn)

    if failed_tests:
        print('')
        print('    There were {num_failures:d} failed PHS2061 fitting tests'.format(num_failures=len(failed_tests)))
    print('')

    return failed_tests

if __name__ == "__main__":
    do_tests()