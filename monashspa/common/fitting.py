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

import random
import traceback

import lmfit
from lmfit.models import LinearModel
import numpy as np
from warnings import warn

class MonashSPAFittingException(Exception):
    pass

def model_fit(model, parameters, x, y, u_y=None, **kwargs):
    """A wrapper for fitting to an arbitrary model using lmfit.

    This function automatically inverts the array of standard errors
    to weights (which lmfit expects) and disables the scaling of the 
    covariant matrix is the array of standard errors are provided.

    Note: Any additional keyword arguments passed to this function
          will be passed directly to :code:`model.fit`.

    Arguments:
        model: a reference to a `lmfit`_ model.

        parameters: a reference to a :py:class:`lmfit.parameters.Parameters`
                    object for your model
        
        x: A 1D numpy array of x data points

        y: A 1D numpy array of y data points

    Keyword Arguments:
        u_y: An optional argument for providing a 1D numpy array of uncertainty 
             values for the y data points
    
    Returns:
        A :py:class:`lmfit.model.ModelResult` object from the `lmfit`_ Python library

    .. _`lmfit`: https://lmfit.github.io/lmfit-py/
    
    """
    # invert u_y because lmfit wants weights not sigma
    if u_y is not None:
        if not isinstance(u_y, np.ndarray):
            u_y = np.array(u_y)
        u_y = 1.0/u_y

        if 'scale_covar' not in kwargs:
            kwargs['scale_covar'] = False

    # if 'nan_policy' not in kwargs:
    #     kwargs['nan_policy'] = 'omit'

    #     # warn if there are any nans!
    #     to_check = [('x', x), ('y', y)]
    #     if u_y is not None:
    #         to_check.append(('u_y',u_y))
    #     for name, arr in to_check:
    #         if np.isnan(arr).any():
    #             warn('The {name} array contains at least one NaN. These data points will be ignored when performing the fit. This may cause problems when plotting the line of best fit (you will need to remove the corresponding point in all arrays).'.format(name=name))
    
    # find number of independent vars that are not in kwargs already
    missing_vars = []
    for var in model.independent_vars:
        if var not in kwargs:
            missing_vars.append(var)
    if len(missing_vars) > 1:
        raise MonashSPAFittingException('You have not passed in all of your independent variables as keyword arguments')
    elif len(missing_vars) == 0:
        x_included = False
        for var in model.independent_vars:
            if kwargs[var] == x:
                x_included = True
                break
        if not x_included:
            raise MonashSPAFittingException('You have passed in a value for the argument "x" but it is apparently not an independent arg of your model.')
    elif len(missing_vars) == 1:
        kwargs[missing_vars[0]] = x 

    try:
        fit_result = model.fit(y, parameters, weights=u_y, **kwargs)
    except ValueError:
        msg = traceback.format_exc()
        msg += '\n'
        msg += 'The fit failed. This is usually either because (a) you did not provide sufficient guesses for the model parameters, (b) you did not correctly specify the independent variable in your model (by default it must be "x"), or (c) the data you are fitting to contains NaN values.'
        raise MonashSPAFittingException(msg)

    return fit_result

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
    guess_kwargs = {}
    # Create parameter guesses
    if slope_guess is not None:
        guess_kwargs['slope'] = slope_guess
    if intercept_guess is not None:
        guess_kwargs['intercept'] = intercept_guess

    initial_parameters = model.guess(y, x=x, **guess_kwargs)

    fit_result = model_fit(model, initial_parameters, x, y, u_y)

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
        try:
            results['u_'+param_name] = param.stderr
        except Exception:
            results['u_'+param_name] = np.nan
    return results

# From https://bitbucket.org/labscript_suite/runmanager
# Code written by Philip Starkey and he has relicensed and contributed
# it as part of this Library
class __TraceDictionary(dict):

    def __init__(self, *args, **kwargs):
        self.trace_data = None
        self.all_accessed_vars = None
        dict.__init__(self, *args, **kwargs)

    def start_trace(self):
        self.trace_data = []
        self.all_accessed_vars = []

    def __getitem__(self, key):
        # only trace things that don't exist
        try:
            dict.__getitem__(self, key)
            self.all_accessed_vars.append(key)
        except Exception:
            if self.trace_data is not None:
                if key not in self.trace_data:
                    self.trace_data.append(key)
        return dict.__getitem__(self, key)

    def stop_trace(self):
        trace_data = self.trace_data
        all_accessed_vars = self.all_accessed_vars
        self.trace_data = None
        self.all_accessed_vars = None
        return trace_data, all_accessed_vars

__unique_fn_id = 1

def make_lmfit_model(expression, independent_vars=None, allow_constant_model=False, **kwargs):
    """A convenience function for creating a lmfit Model from an equation in a string

    This function takes an expression containing the right hand side of an
    equation you wish to use as your fitting model, and generates a
    :py:class:`lmfit.model.Model` object from the `lmfit`_ Python library

    For example, the expression :code:`"m*x+c"` would create a model that
    would fit to linear data modelled by the equation :math:`y=m*x+c`.
    Note that the expression does not contain the :code:`y` or :code:`=`
    symbols 
    
    Standard numpy and scipy.special functions are also available for use 
    in your expression.
    For example, this is also a valid expression: :code:`"sin(x)+c"`.

    The expression must always be valid Python code, and must be able to 
    be evaluated with every parameter set to a random floating point number.

    The independent variable is assumed to be :code:`x` unless otherwise
    specified. All other variables are assumed to be parameters you wish
    the fitting routine to optimise. These parameters will be given an initial
    hint of 1 in the returned model, but can be overridden later using 
    :py:meth:`lmfit.model.Model.set_param_hint`,
    :py:meth:`lmfit.model.Model.make_params`, or 
    :py:meth:`lmfit.parameter.Parameters.add`.

    Note: Additional keyword arguments are passed directly to 
    :py:class:`lmfit.model.Model`.

    Arguments:
        expression: A string containing the right-hand-side of the equation
                    you wish to model (assumes the left hand side is equal
                    to "y").

    Keyword Arguments:
        independent_vars: a list of independent variable names that should
                          not be varied by lmfit. If set to :code:`None`
                          (the default) it assumes that the independent
                          variables is just :code:`["x"]`
        
        allow_constant_model: A Boolean to indicate whether to suppress the 
                              exception raised if you don't use the independent
                              variable(s) in your model equation. Defaults to 
                              :code:`False` (raise the exception). If you do 
                              wish to use a constant model, we recommend
                              leaving this as "False" and modifying your model
                              equation to include an "x*0" (or similar) term as
                              this also ensures the component can be plotted
                              using 
                              :py:meth:`lmfit.model.ModelResult.eval_components` 
                              without additional modification. However, you can 
                              also set this to :code:`True` to suppress the 
                              Exception and restore the default lmfit behaviour.

    Returns:
        A :py:class:`lmfit.model.Model` object to be used for fitting with
        the lmfit library.

    .. _`lmfit`: https://lmfit.github.io/lmfit-py/
    
    """

    global __unique_fn_id

    # assume "x" if not specified
    if independent_vars is None:
        independent_vars = ["x"]
    # ensure it's a list!
    elif not isinstance(independent_vars, list):
        independent_vars = list(independent_vars)

    # detect the parameter names in the expression if they are not provided
    sandbox = __TraceDictionary()
    # provide some basic numpy functionality
    __model_sandbox_imports(sandbox)

    # warn if the independent vars are named after things that already exist in sandbox
    for param in independent_vars:
        if param in sandbox:
            warn('\nYour independent variable "{}" shares a name with an item in the numpy or scipy libraries. This may cause unexpected behaviour. Please use something unique, such as "x".\n\n'.format(param))

    # keep a list of parameters we should randomise every iteration 
    # (to prevent things like divide by 0 exceptions!)
    params_to_randomise = []
    params_to_randomise.extend(independent_vars)

    keep_trying = 5
    success = False
    while not success:
        # set random values for each parameter we know about so far
        for param in params_to_randomise:
            r = random.random()*10
            if random.random() < 0.05:
                r += random.random()*1000
            sandbox[param] = r

        # attempt to evaluate the expression
        sandbox.start_trace()
        try:
            code = compile(expression, '<string>', 'eval')
            eval(code, sandbox)
        except TypeError:
            params, _ = sandbox.stop_trace()

            problem_param = None
            if params_to_randomise is not None:
                if params_to_randomise[-1] not in independent_vars:
                    problem_param = params_to_randomise[-1]
            if problem_param is None:
                for param in params:
                    if param not in params_to_randomise:
                        problem_param = param
            if problem_param is None:
                problem_param = "[Could not determine the parameter name]"

            raise RuntimeError('Error occurred while evaluating the model function. The problem is likely with the use of "{var}" which is either an unknown function or a parameter that cannot be set to a floating point number.'.format(var=problem_param))
        except Exception:
            # An exception was raised! This is either because:
            #   We found a new parameter name (great!)
            #   The expression has an error (Bad!)
            #
            # So we get the params found in this evaluation, and
            # see if any are new
            params, _ = sandbox.stop_trace()
            original_length = len(params_to_randomise)
            for param in params:
                if param not in params_to_randomise:
                    params_to_randomise.append(param)

            # decide whether we keep going or not depending on whether
            # we found a new parameter
            if len(params_to_randomise) == original_length:
                keep_trying -= 1
            else:
                keep_trying += 1

            if keep_trying <= 0:
                raise
            else:
                continue
        
        # if we get to here, everything evaluated!
        success = True
        params, all_params = sandbox.stop_trace()
        for param in params:
            if param not in params_to_randomise:
                params_to_randomise.append(param)

        # check if all of the independent variables are used as a parameter
        for param in independent_vars:
            if param not in all_params:
                if not allow_constant_model:
                    raise MonashSPAFittingException('You have not used the independent variable "{param}" in your model "{model}". Have you accidentally used a different variable name for your independent variable? This may produce unexpected results. Please update your model so that is is defined as a function of "{param}". If you are certain your model is correct, then you can suppress this exception by passing the optional argument "allow_constant_model=True" to the call to make_lmfit_model().'.format(param=param, model=expression))
    
    # params_to_randomise now contains everything we need!

    # provide a nice model function name
    # use prefix if it is provided to lmfit, or a unique incrementing name
    if 'prefix' in kwargs:
        fn_name = kwargs['prefix']
    else:
        fn_name = "custom_model_function_{:d}".format(__unique_fn_id)
        __unique_fn_id += 1

    # construct the function code in a string
    code_str = "def {:s}(".format(fn_name)
    for i, param in enumerate(params_to_randomise):
        code_str += param
        if i < len(params_to_randomise)-1:
            code_str += ", "
    code_str += "): return {expression}".format(expression=expression)

    # create fresh sandbox with standard imports
    sandbox = {}
    __model_sandbox_imports(sandbox)
    # compile our function code
    code = compile(code_str, 'model.py', 'exec')
    # execute it in the sandbox
    exec(code, sandbox, sandbox)
    # extract the model function and create the model
    model_fn = sandbox[fn_name]
    model = lmfit.models.Model(model_fn, independent_vars=independent_vars, **kwargs)

    # set default parameter hints that are not just -Inf
    for param in params_to_randomise:
        if param not in independent_vars:
            model.set_param_hint(param, value=1)

    return model

def __model_sandbox_imports(sandbox):
    # scipy functions
    exec('from scipy.special import *', sandbox, sandbox)
    exec('import scipy.special', sandbox, sandbox)
    # numpy functions (will overwrite some scipy in global namespace)
    # but the scipy ones will also be available through scipy.special.<function>
    exec('from numpy import *', sandbox, sandbox)
    exec('import numpy as np', sandbox, sandbox)