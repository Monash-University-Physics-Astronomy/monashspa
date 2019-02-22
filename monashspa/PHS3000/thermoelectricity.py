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
    """Reads the csv file produced by the thermoelectricity software

    Arguments:
        filepath: The path to the .csv file

    Returns:
        A 2D numpy array containing the data from the file, with columns
        date-time, delta_t from row 0, T_Cold, T_Hot, T_Case, I_Heat, V_Heat,
        I_Pelt, V_Pelt, respectively.

    """

    df = pandas.read_csv(filepath, parse_dates={'Datetime':[0,1]})

    # convert to numpy array
    arr = df.to_numpy()

    # calculate timedeltas
    time_delta = np.zeros((arr.shape[0],))

    # vectorise the conversion to total seconds
    f = np.vectorize(lambda x: x.total_seconds())

    # calculate the timedelta column
    time_delta[1:] = f(arr[1:,0]-arr[0,0])

    # insert the timedelta column at column 1
    arr = np.insert(arr, 1, time_delta, axis=1)

    return arr