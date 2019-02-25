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