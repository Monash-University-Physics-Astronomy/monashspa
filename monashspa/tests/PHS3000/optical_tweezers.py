import numpy as np

def test_k_trap_theory():
    """Basic test of PHS3000 optical tweezers function k_trap_theory"""

    ### Get results ###
    from monashspa.PHS3000 import optical_tweezers as op

    # f,psx,psy = op.ps_load(r'Example data\1\40mA.lvm')
    # fc1=op.cf_linearised(f,psx,100, show_plots=False)
    # fc2=op.cf_linearised(f,psy,100)
    # print(fc1, fc2)

    result = op.trap_k_theory(1.5e-6, 3.2e-7, (1.58**2/1.33**2-1), 3, 5251802272)
    expected_result = 2.6373474496644467e-06
    precision = 1e-12

    success = True
    if np.abs(result-expected_result) > precision:
        success = False

    return success

def do_tests():
    tests = [test_k_trap_theory, ]
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