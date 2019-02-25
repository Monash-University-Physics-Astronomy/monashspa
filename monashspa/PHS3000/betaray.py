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
    """Reads the csv file produced by the betaray online experiment

    Arguments:
        filepath: The path to the .csv file

    Returns:
        A 2D numpy array containing the data from the file, with columns
        Acquisition time, Run mode, Vacuum pressure, Shutter Position, Duration (s), Count, Lens coil current (A), u(Lens coil current) (A), Bias coil current (A), u(Bias coil current) (A), Magnetometer x position, Magnetometer y position, Magnetometer x-axis field strength (µT), u(Magnetometer x-axis field strength) (µT), Magnetometer y-axis field strength (µT), u(Magnetometer y-axis field strength) (µT), Magnetometer z-axis field strength (µT), and u(Magnetometer z-axis field strength) (µT) respectively.

    """

    df = pandas.read_csv(filepath, parse_dates=[0])

    # convert to numpy array
    arr = df.to_numpy()

    return arr

#: The modified Fermi function, :math:`G`, for :math:`Z=55`.
#: Here, the first column corresponds to momentum, :math:`p`, in relativistic 
#: units of :math:`m_0 c^2` and the second column cooresponds to the value of
#: the modified Fermi function :math:`G`.
modified_fermi_function_data = np.array([
    [0.0, 6.591],
    [0.1, 6.582],
    [0.2, 6.552],
    [0.3, 6.506],
    [0.4, 6.448],
    [0.5, 6.387],
    [0.6, 6.329],
    [0.7, 6.275],
    [0.8, 6.224],
    [0.9, 6.177],
    [1.0, 6.132],
    [1.2, 6.046],
    [1.4, 5.964],
    [1.6, 5.886],
    [1.8, 5.812],
    [2.0, 5.742],
    [2.2, 5.675],
    [2.4, 5.612],
    [2.6, 5.553],
    [2.8, 5.496],
    [3.0, 5.443],
])