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

import pandas
import numpy as np

def read_data(filepath):
    """Imports the 'xls' file (actually just a tsv) save by the Rigol Oscilloscope software

    Arguments:
        filepath: The path to the .xls or .txt file produced by the Rigol
                  oscilloscope software

    Returns:
        A tuple :code:`(t, V)` where :code:`t` is a 1D numpy array
        containing the time values associated with the oscilloscope trace
        and :code:`V` is a 1D numpy array of the same length with the associated
        voltage readings for each time point.

    """
    # TODO: consider replacing with our own csv reading wrapper
    df = pandas.read_csv(filepath, skiprows=list(range(7))+[8,], sep='\t')

    t = df[df.columns[1]].values
    V = df[df.columns[2]].values

    return t, V