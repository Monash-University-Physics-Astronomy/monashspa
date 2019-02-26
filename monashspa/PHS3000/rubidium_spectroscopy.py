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
import six

def __matlab_round(val):
    if six.PY2:
        return round(val)
    else:
        import decimal
        return int(decimal.Decimal(val).quantize(decimal.Decimal('1'), 
    rounding=decimal.ROUND_HALF_UP))

def read_rigol_csv(filepath):
    """Reads the csv file saved from the Rigol digital storage oscilloscope.
    
    Arguments:
        filepath: A string containing the path to the csv file

    Returns:
        A tuple :code:`(X, time, CH1, CH2)` where each element is a 1D numpy 
        array containing an array of incrementing integers, an array of time 
        points (x-axis of the oscilloscope), and the y-values for channels 1
        and 2 respectively.
    """

    # read the data (skip the second line, and only use first 3 columns)
    df = pandas.read_csv(filepath, skiprows=[1], usecols=[0,1,2])

    X = df[df.columns[0]].values
    CH1 = df[df.columns[1]].values
    CH2 = df[df.columns[2]].values

    # now read the information poorly encoded in the header
    df = pandas.read_csv(filepath, nrows=1, usecols=[3,4])
    
    dt = df[df.columns[1]].values[0]
    time = X*dt

    return X, time, CH1, CH2

def extract_frequency(michelson_data, MHz_per_fringe, num_dc_terms_to_remove=1):
    """Returns a frequency calibration determined from Michelson interferometer data
    
    Performs a Hilbert transform (minus the DC term) on the Michelson
    interferometer data and scales the resultant frequency array by the
    distance (in MHz) between constructive interference fringes.
    
    Arguments:
        michelson_data: A 1D numpy array containing the oscilloscope data 
                        from the michelson interferometer

        MHz_per_fringe: The distance (in MHz) between constructive interference
                        fringes in the :code:`michelson_data` calculated from
                        the path length difference of the Michelson 
                        interferometer arms.

    Keyword Arguments:
        num_dc_terms_to_remove: The number of low frequency components to remove
                                after performing the Fourier transform. The 
                                default is 1 (remove the DC term only). Higher 
                                integers remove low order frequency components
    
    Returns:
        A 1D numpy array (with the same length as :code:`michelson_data`)
        containing a frequency calibration (in MHz) for the saturated absorption 
        spectra. Use this array as the x-axis for plotting and fitting.
    """
    ffty = np.fft.fft(michelson_data)
    subffty = np.zeros(michelson_data.shape, dtype=np.complex128)
    subffty[__matlab_round(num_dc_terms_to_remove):__matlab_round(len(michelson_data)/2)+1] = ffty[__matlab_round(num_dc_terms_to_remove):__matlab_round(len(michelson_data)/2)+1]
    back = np.fft.ifft(subffty)
    return np.unwrap(np.angle(back))/(2*np.pi)*MHz_per_fringe
    