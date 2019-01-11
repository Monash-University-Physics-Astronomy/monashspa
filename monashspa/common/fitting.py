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

from lmfit.models import LinearModel
import numpy as np

class MonashSPAFittingException(Exception):
    pass


def linear_fit(x, y, u_y=None, slope_guess=None, intercept_guess=None):
    """ General purpose linear fit function.

    This function takes your x and y data (as numpy arrays) and returns a
    :py:class:`lmfit.model.ModelResult` object from the `lmfit`_ Python library.
    It attempts to fit your data to a model define by:
        :math:`y=mx+c`
    where :math:`m = slope` and :math:`c = intercept`.
    If guesses for the slope and intercept are not explicitly provided when
    calling this function, they will be inferred from the provided data arrays.

    Arguments:
        x: A 1D numpy array of x data points

        y: A 1D numpy array of y data points

    Keyword Arguments:
        u_y: An optional argument for providing a 1D numpy array of uncertainty 
             values for the y data points

        slope_guess: An optional argument for providing an initial guess for the
                     value of the slope parameter

        intercept_guess: An optional argument for providing an initial guess for the
                         value of the intercept parameter

    Returns:
        A :py:class:`lmfit.model.ModelResult` object from the `lmfit`_ Python library

    .. _`lmfit`: https://lmfit.github.io/lmfit-py/

    """
    # Create Model
    model = LinearModel()
    a=1
    guess_kwargs = {}
    # Create parameter guesses
    if slope_guess is not None:
        guess_kwargs['slope'] = slope_guess
    if intercept_guess is not None:
        guess_kwargs['intercept'] = intercept_guess

    initial_parameters = model.guess(y, x=x, **guess_kwargs)

    # invert u_y because lmfit wants weights not sigma
    if u_y is not None:
        if not isinstance(u_y, np.ndarray):
            u_y = np.array(u_y)
        u_y = 1.0/u_y

    kwargs = {}
    if u_y is not None:
        kwargs['scale_covar'] = False

    fit_result = model.fit(y, initial_parameters, x=x, weights=u_y, **kwargs)

    if not fit_result.success:
        raise MonashSPAFittingException("The call to 'linear_fit(...)' failed. Perhaps try specifying a good guess for the 'gradient_guess' and/or 'intercept_guess' keyword arguments? The error message returned by the fitting algorithm was: {error}".format(error = fit_result.message))

    return fit_result

def get_fit_parameters(fit_result):
    """ Returns the parameters from a fit result as a dictionary.

    This function takes a :py:class:`lmfit.model.ModelResult` object from the
    `lmfit`_ Python library and extracts the parameters of the fit along with
    their uncertainties. These are returned to you in a Python dictionary
    format. The format of the dictionary depends on the model used to perform
    the fit. For example, a linear fit would result in the following 
    dictionary:
        .. code-block:: python

            parameters = {
                'slope': <value>,
                'u_slope': <value>,
                'intercept': <value>,
                'u_intercept': <value>,
            }


    The parameter names always match those of the lmfit model, and the
    uncertainties are always the identical parameter name prefixed with
    :code:`u_`.

    Arguments:
        fit_result: A :py:class:`lmfit.model.ModelResult` object from the
                    `lmfit`_ Python library.

    Returns:
        A dictionary containing the fit parameters and their associated 
        uncertainties.

    .. _`lmfit`: https://lmfit.github.io/lmfit-py/

    """
    results = {}
    for param_name, param in fit_result.params.items(): 
        results[param_name] = param.value
        results['u_'+param_name] = param.stderr
    return results
