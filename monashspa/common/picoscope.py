# Copyright 2019 School of Physics & Astronomy, Monash University),
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

def read_picoscope_csv(filepath):
    """Reads the csv file saved from the PicoScope software
    
    .. note:: The picoscope software will save overrange values in the csv file
              as either "Infinity" or the unicode symbol for infinity (which 
              will show up in some software as several random characters). This
              Python function converts those instances to :code:`np.nan`.

    .. note:: This function attempts to return values in S.I. units without a 
              prefix. For example, if the csv file contains time in 
              milliseconds, this function will attempt to detect that and return 
              the data in units of seconds. If the function fails to make this 
              conversion, a warning message will be printed.

    Arguments:
        filepath: A string containing the path to the csv file

    Returns:
        A tuple :code:`(time, CHA, CHB)` where each element is a 1D numpy 
        array containing an array of time 
        points (x-axis of the oscilloscope), and the y-values for channels A
        and B respectively. The units of these should be seconds, Volts and 
        Volts respectively unless otherwise stated via a warning message 
        printed to your terminal.
    """

    # read the data (skip the second line, and only use first 3 columns)
    df = pandas.read_csv(filepath, skiprows=[1,2], usecols=[0,1,2], na_values=['Infinity', '-Infinity', '\u221e', '-\u221e'])

    time = df[df.columns[0]].values
    CHA = df[df.columns[1]].values
    CHB = df[df.columns[2]].values

    # now read the units
    df = pandas.read_csv(filepath, nrows=2, usecols=[0,1,2])
    
    time_unit = df[df.columns[0]].values[0]
    CHA_unit = df[df.columns[1]].values[0]
    CHB_unit = df[df.columns[2]].values[0]

    if time_unit == '(ms)':
        time = time * 1e-3
    elif time_unit == '(s)':
        pass
    elif time_unit == '(us)':
        time = time * 1e-6
    else:
        print('Warning: Unknown unit for time. Do not assume time is in seconds. It is in {}'.format(time_unit))

    if CHA_unit == '(mV)':
        CHA = CHA * 1e-3
    elif CHA_unit == '(V)':
        pass
    elif CHA_unit == ('uV'):
        CHA = CHA * 1e-6
    else:
        print('Warning: Unknown unit for CHA. Do not assume CHA is in Volts. It is in {}'.format(CHA_unit))

    if CHB_unit == '(mV)':
        CHB = CHB * 1e-3
    elif CHB_unit == '(V)':
        pass
    elif CHB_unit == ('uV'):
        CHB = CHB * 1e-6
    else:
        print('Warning: Unknown unit for CHB. Do not assume CHB is in Volts. It is in {}'.format(CHB_unit))

    return time, CHA, CHB