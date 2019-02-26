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

def test_k_trap_theory():
    """Basic test of PHS3000 optical tweezers function k_trap_theory"""

    ### Get results ###
    from monashspa.PHS3000 import optical_tweezers as op

    result = op.trap_k_theory(1.5e-6, 3.2e-7, (1.58**2/1.33**2-1), 3, 5251802272)
    expected_result = 2.6373474496644467e-06
    precision = 1e-12

    success = True
    if np.abs(result-expected_result) > precision:
        success = False
    if not success:
        print(' '*8 + 'Value is not within tolerance.')
        print(' '*(8+4) + 'Expected value: {}'.format(expected_result))
        print(' '*(8+4) + 'Actual value: {}'.format(result))
        print(' '*(8+4) + 'Tolerance: {}'.format(precision))

    return success

def test_k_trap_theory_array():
    """Test of PHS3000 optical tweezers function k_trap_theory with array input for r"""

    ### Get results ###
    from monashspa.PHS3000 import optical_tweezers as op

    r = np.array([1.5e-6, 2e-6, 3.1e-6])
    result = op.trap_k_theory(r, 3.2e-7, (1.58**2/1.33**2-1), 3, 5251802272)
    expected_result = np.array([2.6373474496644467e-06, 7.146758330328241e-07, 2.1117891093096543e-08])
    precision = 1e-12

    success = expected_result.shape == result.shape
    if not np.all(np.isclose(expected_result, result, atol=precision)):
        success = False
    if not success:
        print(' '*8 + 'Values are not within tolerance.')
        print(' '*(8+4) + 'Expected value: {}'.format(expected_result))
        print(' '*(8+4) + 'Actual value: {}'.format(result))
        print(' '*(8+4) + 'Tolerance: {}'.format(precision))

    return success

def test_k_trap_theory_array_multiple():
    """Test of PHS3000 optical tweezers function k_trap_theory with array input for r and w"""

    ### Get results ###
    from monashspa.PHS3000 import optical_tweezers as op

    r = np.array([1.5e-6, 2e-6, 3.1e-6])
    w = np.array([3.2e-7, 2e-7, 8e-7])
    result = op.trap_k_theory(r, w, (1.58**2/1.33**2-1), 3, 5251802272)
    expected_result = np.array([2.6373474496644467e-06, 9.069896532126502e-09, 1.2885130290016302e-05])
    precision = 1e-12

    success = expected_result.shape == result.shape
    if not np.all(np.isclose(expected_result, result, atol=precision)):
        success = False
    if not success:
        print(' '*8 + 'Values are not within tolerance.')
        print(' '*(8+4) + 'Expected value: {}'.format(expected_result))
        print(' '*(8+4) + 'Actual value: {}'.format(result))
        print(' '*(8+4) + 'Tolerance: {}'.format(precision))

    return success

def do_tests():
    tests = [test_k_trap_theory, test_k_trap_theory_array, test_k_trap_theory_array_multiple]
    failed_tests = []
    print('Running PHS3000 optical tweezers tests...')

    for testfn in tests:
        print('    Running test "{test_name}":'.format(test_name=testfn.__doc__))
        result = testfn()
        print('        Result: {result}'.format(result='success' if result else 'failure'))

        if not result:
            failed_tests.append(testfn)

    if failed_tests:
        print('')
        print('    There were {num_failures:d} failed PHS3000 optical tweezers tests'.format(num_failures=len(failed_tests)))
    print('')

    return failed_tests

if __name__ == "__main__":
    do_tests()