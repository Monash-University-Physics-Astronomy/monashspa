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

import os

import numpy as np
import pandas
import matplotlib.pyplot as plt
import lmfit
from lmfit.models import QuadraticModel as __QuadraticModel
import scipy.special


from monashspa.PHS3000 import linear_fit as __linear_fit
from monashspa.common.fitting import MonashSPAFittingException as __MonashSPAFittingException

def trap_k_theory(r, w, alpha, eccentricity, I):
    r"""Calculates the theoretical spring constant (:math:`k`) for an optical tweezers trap for specified parameters

    Calculates using the equation:
        :math:`k=\alpha\,I_0\,\omega\,\frac{2\,\pi\,\epsilon^3}{c\,\xi^3}\left(\sqrt{\frac{\pi}{2}}\,\left(\left(\frac{\xi\,a}{\epsilon}\right)^2-1\right)\,\mathrm{exp}\left[-\frac{a^2}{2}\right]\,\mathrm{erf}\left[\frac{\xi\,a}{\sqrt{2}\,\epsilon}\right]+\frac{\xi\,a}{\epsilon}\,\mathrm{exp}\left[-\frac{a^2}{2\,\epsilon^2}\right]\right)`
    from `Bechhoefer 2002`_.

    If the input arguments are numpy arrays, then the output will also be an
    array of the appropriate dimension. Otherwise a single number will be 
    returned.

    Arguments:
        r: Sphere radius (m)
        w: The :math:`1/e^2` radius (beam waist) of the trapping beam (m)
        alpha: :math:`n_p^2/n_0^2 - 1`, where :math:`n_p` is the refractive 
               index of the microsphere and :math:`n_0` is the refractive index
               of water
        eccentricity: The eccentiricty of the trapping beam
        I: Trapping beam intensity (W/m^2)

    Returns:
        k: The theoretical spring constant (:math:`k`)

    .. _`Bechhoefer 2002`: http://scitation.aip.org.ezproxy.lib.monash.edu.au/content/aapt/journal/ajp/70/4/10.1119/1.1445403

    """
    
    # calculate a
    a = r/w

    # Make eccentricity complex so that numpy can handle the sqrt
    eccentricity = eccentricity + 0j
    xi = np.sqrt(1-eccentricity**2)
    
    # define speed of light
    c = 299792458

    # calculate k
    k = alpha/c*I*w*2*np.pi*eccentricity**3/xi**3*(
            np.sqrt(np.pi/2)*((xi*a/eccentricity)**2-1)*np.exp(-a**2/2)*scipy.special.erf(xi*a/(np.sqrt(2)*eccentricity)) 
            + (xi*a/eccentricity)*np.exp(-a**2/(2*eccentricity**2))
        )

    # if the imaginary component is 0 (which it should be), then return only
    # the real component. Otherwise, return the whole complex number
    if isinstance(k, np.ndarray):
        return np.real_if_close(k)
    else:
        return k.real if k.imag == 0 else k

def ps_load(filepath):
    """Imports the power spectrum data from optical tweezers file

    Arguments:
        filepath: The path to the .lvm file produced by the optical tweezers
                  acquisition software

    Returns:
        A tuple :code:`(f, psx, psy)` where :code:`f` is a 1D numpy array
        containing the frequency values associated with the power spectrums
        in :code:`psx` and :code:`psy` (which are also both 1D numpy arrays).

    """
    # TODO: consider replacing with our own csv reading wrapper
    df = pandas.read_csv(filepath, skiprows=22, sep='\t')
    f = df[df.columns[8]].values
    psx = df[df.columns[9]].values
    psy = df[df.columns[11]].values

    # strip out NaNs (as these columns are shorter than the others)
    f = f[~np.isnan(f)]
    psx = psx[~np.isnan(psx)]
    psy = psy[~np.isnan(psy)]

    return f, psx, psy

def cf_linearised(f, ps, initial_fc, call_show = True):
    r"""Finds the corner frequency value for a lorentzian power spectrum

    Finds the corner frequency (:math:`f_c`) of a power spectrum of the form:
        :math:`y=\frac{a}{(f_c^2+f^2)}`
    by transforming into the logarithmic domain and determining when the 
    spectrum is linearised.

    Arguments:
        f: A 1D numpy array containing the frequency values associated with 
           the power spectrum
        ps: A 1D numpy array containing the power spectrum data (must be the
            same length as :code:`f`)
        initial_fc: An initial guess for the corner frequency

    Keyword Arguments:
        call_show: Whether to call :code:`matplotlib.pyplot.show()` at the end
                   of the function (prior to returning). Defaults to :code:`True`.
                   Set this to :code:`False` if you are not using Spyder/IPython
                   and wish your entire script to complete before showing any 
                   plots. Note, you will need to explicitly call 
                   :code:`matplotlib.pyplot.show()` if you set this to :code:`False`.
    
    Returns:
        The best estimate for the corner frequency :math:`f_c`.

    """
    y = np.log(ps)

    plt.figure()
    plt.loglog(f,ps)
    plt.title('Power spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'Power Spectral Density ($V^2$/Hz)')
    
    # remove first 2 terms
    y = y[2:]
    f = f[2:]
    ps = ps[2:]

    params = lmfit.Parameters()
    params.add('a', y[0])
    params.add('fc', initial_fc)
    result = lmfit.minimize(__cf_linearised_search, params, method='nelder', args=(f,y))
    fc = result.params['fc'].value

    plt.figure()
    plt.semilogy(np.log(fc**2+f**2), ps)
    plt.title('Linearised Power Spectrum Analysis')
    plt.xlabel(r'$f_0^2+f^2$ ($Hz^2$)')
    plt.ylabel(r'Power Spectral Density ($V^2$/Hz)')

    if call_show:
        plt.show()

    return fc

def __cf_linearised_search(params, f, y):
    parvals = params.valuesdict()
    a = parvals['a']
    fc = parvals['fc']

    out = a - np.log(fc**2+f**2)

    # do linear fit
    linear_result = __linear_fit(out, y)

    # do quadratic fit
    quadratic_result = __quadratic_fit(out, y)

    e = linear_result.best_fit - quadratic_result.best_fit
    return np.matmul(np.transpose(e), e)

def __quadratic_fit(x, y):
    """Special purpose quadratic fit for optical tweezers

    Arguments:
        x: A 1D numpy array of x data points

        y: A 1D numpy array of y data points

    Returns:
        A :py:class:`lmfit.model.ModelResult` object from the `lmfit`_ Python library

    .. _`lmfit`: https://lmfit.github.io/lmfit-py/

    """
    # Create Model
    model = __QuadraticModel()
    initial_parameters = model.guess(y, x=x)
    fit_result = model.fit(y, initial_parameters, x=x)

    if not fit_result.success:
        raise __MonashSPAFittingException("Failed to perform the quadratic fit step. The error message returned by the fitting algorithm was: {error}".format(error = fit_result.message))

    return fit_result