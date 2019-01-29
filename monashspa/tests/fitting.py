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
    #
    # check same number of results returned as expected
    success = len(expected_results) == len(results)
    
    # iterate over every result
    for k,v in results.items():
        # check key names match
        if k not in expected_results:
            success = False
            break
        # Check result is within tolerance to expected value
        if np.abs(expected_results[k] - v) > precision:
            success = False
            break

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
    #
    # check same number of results returned as expected
    success = len(expected_results) == len(results)

    # iterate over every result
    for k,v in results.items():
        # check key names match
        if k not in expected_results:
            success = False
            break
        # Check result is within tolerance to expected value
        if np.abs(expected_results[k] - v) > precision:
            success = False
            break

    return success

def do_tests():
    tests = [test_basic_linear_fit, test_linear_fit_with_uncertainties]
    failed_tests = []

    for testfn in tests:
        result = testfn()
        print('Result of "{test_name}" was {result}'.format(test_name=testfn.__doc__, result='success' if result else 'failure'))

        if not result:
            failed_tests.append(testfn)

    if failed_tests:
        print('')
        print('There were {num_failures:d} failed fitting tests'.format(num_failures=len(failed_tests)))

    return failed_tests

if __name__ == "__main__":
    do_tests()