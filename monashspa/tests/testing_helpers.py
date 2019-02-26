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

def compare_dictionary(results, expected_results, tolerance, indent=8):
    # check same number of results returned as expected
    success = len(expected_results) == len(results)
    
    # iterate over every result
    for k,v in results.items():
        # check key names match
        if k not in expected_results:
            success = False
            print(' '*indent + 'Key "{key}" missing from expected results'.format(key=k))
        # Check result is within tolerance to expected value
        if np.abs(expected_results[k] - v) > tolerance:
            success = False
            print(' '*indent + 'Values for "{key}" are not within tolerance.'.format(key=k))
            print(' '*(indent+4) + 'Expected value: {}'.format(expected_results[k]))
            print(' '*(indent+4) + 'Actual value: {}'.format(v))
            print(' '*(indent+4) + 'Tolerance: {}'.format(tolerance))
            print(' '*(indent+4) + 'Difference: {}'.format(np.abs(expected_results[k] - v)))

    # this check technically isn't needed because we compare length and check if
    # all of one is in the other, however this allows us to provide more useful
    # feedback on failed tests
    for k,v in expected_results.items():
        if k not in results:
            success = False
            print(' '*indent + 'Key "{key}" missing from results'.format(key=k))

    return success