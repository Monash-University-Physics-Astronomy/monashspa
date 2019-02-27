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

from __future__ import division

import os

import numpy as np
import pandas
import matplotlib.pyplot as plt
from piradon import iradon as __iradon

def pet_rebuild(filepath, filter_name=None, npoints=None, call_show=True):
    """Perform inverse radon transform on acquired PET data and plots results

    Arguments:
        filepath: A string containing the path to the txt file containing the 
                  PET data
    
    Keyword Arguments:
        filter_name: A string containing the name of the filter to use during
                     reconstruction. Defaults to :code:`None` (no
                     reconstruction). Options are:
                        - None: don't reconstruct
                        - 'none': Reconstruct with no filter
                        - 'ramp': Reconstruct using the Ram-Lak filter
                        - 'Shepp-Logan': Reconstruct using the Shepp-Logan filter
                        - 'cosine': Reconstruct using the cosine filter
                        - 'hamming': Reconstruct using the hamming filter
                        - 'hann': Reconstruct using the hann filter

        npoints: The number of points to reconstruct

        call_show: Whether to call :code:`matplotlib.pyplot.show()` at the end
                   of the function (prior to returning). Defaults to :code:`True`.
                   Set this to :code:`False` if you are not using Spyder/IPython
                   and wish your entire script to complete before showing any 
                   plots. Note, you will need to explicitly call 
                   :code:`matplotlib.pyplot.show()` if you set this to :code:`False`. 
    
    Returns:
        A 2D numpy array containing the coincidence counts (rows correspond to
        each linear stage position and columns to each rotation stage position)

    """

    # TODO: consider replacing with our own csv reading wrapper
    df = pandas.read_csv(filepath, skiprows=1, sep=',\t', engine='python', parse_dates=[0])

    # acquisition_time = df[df.columns[0]].values
    rotations = df[df.columns[1]].values
    positions = df[df.columns[2]].values
    coincidence_counts = df[df.columns[3]].values

    # determine number of points in each axis of the scan
    unique_angles = np.unique(rotations)
    unique_positions = np.unique(positions)

    # reshape coincident counts array
    #
    # Note: The array dimensions are swapped between MATLAB and Python.
    #       This avoids the need to transpose as you do in MATLAB because 
    #       of the different scan order during reshape between MATLAB and 
    #       Python. See: https://docs.scipy.org/doc/numpy-1.15.0/user/numpy-for-matlab-users.html#notes
    coincidence_counts.shape = (len(unique_positions), len(unique_angles))

    plt.figure()
    plt.imshow(coincidence_counts, extent=[np.min(unique_angles), np.max(unique_angles), np.max(unique_positions), np.min(unique_positions)], interpolation='none')
    plt.xlabel(r'$\theta$')
    plt.ylabel('x')
    plt.title('Sinogram of {filename}'.format(filename=os.path.basename(filepath)))

    # do the inverse transform
    if filter_name is not None:
        if npoints is None:
            raise RuntimeError('When calling pet_rebuild with a filter, you must specify the number of points to reconstruct')

        # convert string none to actual None
        if filter_name == 'none':
            filter_name = None
        inverse = __iradon(coincidence_counts, unique_angles, output_size=npoints, filter=filter_name, interpolation='linear', circle=False)

        plt.figure()
        plt.imshow(inverse, extent=[0, 1, 0, 1], interpolation='none')
        plt.title('Reconstruction of {filename}'.format(filename=os.path.basename(filepath)))

    if call_show:
        plt.show()

    return coincidence_counts
