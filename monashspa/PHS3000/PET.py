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
from skimage.transform import iradon
import matplotlib.pyplot as plt

def pet_rebuild(filepath, filter_name=None, npoints=None):
    """TODO: write this"""

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

    plt.figure(1)
    plt.imshow(coincidence_counts, extent=[np.min(unique_angles), np.max(unique_angles), np.max(unique_positions), np.min(unique_positions)], interpolation='none')
    plt.xlabel(r'$\theta$')
    plt.ylabel('x')
    plt.title('Sinogram of {filename}'.format(filename=os.path.basename(filepath)))


    # do the inverse transform
    if filter_name is not None:
        # convert string none to actual None
        if filter_name == 'none':
            filter_name = None
        inverse = iradon(coincidence_counts, unique_angles, output_size=npoints, filter=filter_name, interpolation='linear')

        plt.figure(2)
        plt.imshow(inverse, extent=[0, 1, 0, 1], interpolation='none')
        plt.title('Reconstruction of {filename}'.format(filename=os.path.basename(filepath)))
        # print(inverse.shape)
        # print(inverse)

    plt.show()

    return coincidence_counts
