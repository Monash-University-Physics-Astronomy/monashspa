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

from lmfit import Model
import numpy as np

class MonashSPAFittingException(Exception):
    pass

def __linear(x, gradient, intercept, **kwargs):
    return gradient*x + intercept

def linear_fit(x, y, u_y=None, gradient_guess=0, intercept_guess=0):
    """ TODO: docstring here
    """
    model = Model(__linear)

    # invert u_y because lmfit expects this for some reason...
    if u_y is not None:
        if not isinstance(u_y, np.ndarray):
            u_y = np.array(u_y)
        u_y = 1.0/u_y

    kwargs = {}
    if u_y is not None:
        kwargs['scale_covar'] = False

    fit_result = model.fit(y, x=x, weights=u_y, gradient=gradient_guess, intercept=intercept_guess, **kwargs)

    if not fit_result.success:
        raise MonashSPAFittingException("The call to 'linear_fit(...)' failed. Perhaps try specifying a good guess for the 'gradient_guess' and/or 'intercept_guess' keyword arguments? The error message returned by the fitting algorithm was: {error}".format(error = fit_result.message))

    results = {}
    for param_name, param in fit_result.params.items(): 
        results[param_name] = param.value
        results['u_'+param_name] = param.stderr
    return results

def create_y_from_linear_fit(x, fit_results):
    """TODO: write docstring
    """
    return __linear(x, **fit_results)