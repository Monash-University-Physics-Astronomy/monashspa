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
    """Basic test of PHS3000 nonlinear fit"""

    ### Get results ###
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_b_data
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
    """Test of PHS3000 nonlinear fit using an independent variable that was not 'x'"""

    ### Get results ###
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_b_data
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
    """Test of PHS3000 linear fit using custom model"""

    ### Get results ###
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_b_data
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
    """Basic test of PHS3000 linear fit"""

    ### Get results ###
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_b_data
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

def linear_fit_dual_custom_model():
    """Test of PHS3000 linear fit using the sum of two custom models"""

    ### Get results ###
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_b_data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model1 = spa.make_lmfit_model("m*x")
    model2 = spa.make_lmfit_model("c+x*0")
    model = model1 + model2
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

def linear_fit_dual_custom_named_model():
    """Test of PHS3000 linear fit using the sum of two custom models with prefixes"""

    ### Get results ###
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_b_data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    model1 = spa.make_lmfit_model("m*x", prefix="m1")
    model2 = spa.make_lmfit_model("c+x*0", prefix="m2")
    model = model1 + model2
    params = model.make_params(m1m=0.04, m2c=5)
    params.add('halflife', expr="-log(2)/m1m")
    params.add('A_0', expr="exp(m2c)")
    fit_results = spa.model_fit(model, params, x=t, y=np.log(A), u_y=u_A/A)
    results = spa.get_fit_parameters(fit_results)

    ### Expected results ###
    expected_results = {
        'm2c': 3.02843895796932,
        'u_m2c': 0.030620495054301592,
        'm1m': -0.004897938859868103,
        'u_m1m': 0.0001633020007207088,
        'halflife': 141.51813658584769,
        'u_halflife': 4.718351025589936,
        'A_0': 20.664948544330286,
        'u_A_0': 0.6327709546990624,
    }
    precision = 1e-5

    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision)

    return success

def non_linear_fit_part_c():
    """Test of PHS3000 non-linear fit to generic multi-model data"""

    ### Get results ###
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_c1_data
    # slice the data into columns
    x = data[:,0]
    y = data[:,1]

    # Define the models
    model1 = spa.make_lmfit_model("A1*exp(-(x-B1)**2/D1**2)", name="Gaussian1")
    model2 = spa.make_lmfit_model("A2*exp(-(x-B2)**2/D2**2)", name="Gaussian2")
    model3 = spa.make_lmfit_model("c+x*0", name="Offset")
    model = model1 + model2 + model3
    params = model.make_params(A1=np.max(y), B1=100, D1=6, A2=np.max(y), B2=160, c=3)
    params.add('D2', expr='D1')
    params.add('FWHM', expr='2*sqrt(log(2)*D1)')
    fit_results = spa.model_fit(model, params, x=x, y=y)
    results = spa.get_fit_parameters(fit_results)

    ### Expected results ###
    expected_results = {
        'A1': 16.58279101985785, 
        'u_A1': 0.351003396364092, 
        'B1': 95.82492417888295, 
        'u_B1': 0.12363799249150613, 
        'D1': 6.705149651134903, 
        'u_D1': 0.1412232821933916, 
        'A2': 13.690661831671, 
        'u_A2': 0.33945028545509237, 
        'B2': 164.19308257427863, 
        'u_B2': 0.1497567729486557, 
        'D2': 6.705149651134903, 
        'u_D2': 0.14122328218157232, 
        'c': 2.636117481366362, 
        'u_c': 0.06764023986252798, 
        'FWHM': 4.311684392863958, 
        'u_FWHM': 0.045406161696634036
    }
    precision = 1e-5

    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision)

    return success

def nonlinear_fit_part_c2():
    """Test of PHS3000 non-linear fit to multi-model nuclear decay data"""
    import monashspa.PHS3000 as spa

    # load the data
    data = spa.tutorials.fitting.part_c2_data
    # slice the data into columns
    t = data[:,0]
    A = data[:,1]
    u_A = data[:,2]

    ag110_model = spa.make_lmfit_model("A_0*exp(-l*x)", prefix="AG110_")
    ag108_model = spa.make_lmfit_model("A_0*exp(-l*x)", prefix="AG108_")
    offset = spa.make_lmfit_model("c+x*0", name="offset")
    model = ag110_model + ag108_model + offset
    params = model.make_params(AG110_A_0=A[0], AG110_l=np.log(2)/t[4], AG108_l=np.log(2)/t[9], c=0)
    params.add('c', min=0, value=0, max=0.1, vary=True)
    params.add('AG110_halflife', expr='log(2)/AG110_l')
    params.add('AG108_halflife', expr='log(2)/AG108_l')
    fit_results = spa.model_fit(model, params, x=t, y=A, u_y=u_A)
    results = spa.get_fit_parameters(fit_results)

    expected_results = {
        'AG110_A_0': 106.62466958768731,
        'u_AG110_A_0': 3.7021128718124436,
        'AG110_l': 0.03272908958050027,
        'u_AG110_l': 0.0019419683658320412, 
        'AG108_A_0': 24.504027101025645, 
        'u_AG108_A_0': 2.492813131791383, 
        'AG108_l': 0.005097263436001847, 
        'u_AG108_l': 0.000586527763335435, 
        'c': 6.436383415431291e-06, 
        'u_c': 0.3624263607727759, 
        'AG110_halflife': 21.178321470112536, 
        'u_AG110_halflife': 1.2566078265666092, 
        'AG108_halflife': 135.98417842489044, 
        'u_AG108_halflife': 15.647316857620634
    }
    precision = 5e-3

    # split off the check for u_c as the precision (variation across platforms) is much worse than everything else.
    # This is to be expected with multi-model non-linear fits.
    u_c_precision = 0.3
    u_c_result = {'u_c':results['u_c']}
    u_c_expected_result = {'u_c':expected_results['u_c']}
    del results['u_c']
    del expected_results['u_c']

    ### Check results match within precision ###
    success = compare_dictionary(results, expected_results, precision) and compare_dictionary(u_c_result, u_c_expected_result, u_c_precision)

    return success

def do_tests():
    tests = [nonlinear_fit, nonlinear_fit_with_independent_as_t, linear_fit, linear_fit_model, linear_fit_dual_custom_model, linear_fit_dual_custom_named_model, non_linear_fit_part_c, nonlinear_fit_part_c2]
    failed_tests = []

    print('Running PHS3000 fitting tutorial tests...')

    for testfn in tests:
        print('    Running test "{test_name}":'.format(test_name=testfn.__doc__))
        result = testfn()
        print('        Result: {result}'.format(result='success' if result else 'failure'))

        if not result:
            failed_tests.append(testfn)

    if failed_tests:
        print('')
        print('    There were {num_failures:d} failed PHS3000 fitting tests'.format(num_failures=len(failed_tests)))
    print('')

    return failed_tests

if __name__ == "__main__":
    do_tests()
