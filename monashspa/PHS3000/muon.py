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
import pandas

def read_data(filepath):
    """Imports data from the muon physics .data file

    Arguments:
        filepath: The path to the .data file produced by the muon
                  acquisition software

    Returns:
        A 2D numpy array containing the data from the file. The first column 
        contains the acquisition intervals and the second column contains the
        timestamps.

    """

    df = pandas.read_csv(filepath, skiprows=0, header=None, sep=' ')
    return df.to_numpy()

def histc(x, bins):
    """Counts the number of times an values in :code:`x` fall between each bin in :code:`bins`.

    This uses the condition :code:`if bins[i] <= x[j] < bins[i+1]: result[i] += 1` 
    for each element in :code:`x`

    Arguments:
        x: The numpy array containing the data to count
        bins: A numpy array defining the bins

    Returns:
        A numpy array containing the number of elements between each bin.


    """
    indicies = np.digitize(x,bins)
    counts = np.zeros(bins.shape)
    for i in indicies:
        counts[i-1] += 1
    return counts