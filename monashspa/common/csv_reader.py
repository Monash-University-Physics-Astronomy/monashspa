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

def read_csv(filepath, *args, **kwargs):
    """ A simple wrapper around the pandas csv reader.

    This function wraps the :py:func:`pandas.read_csv` function and returns
    a numpy array. Any optional argument for the pandas function can be used 
    here.
    
    Examples
    ^^^^^^^^
    Standard csv files with a header row can be read using 
    :code:`read_csv(filepath)`.

    If your csv file has no header row, use: 
    :code:`read_csv(filepath, header=None)`.

    If your file is delimited by something other than a comma, you can specify
    the separator with the optional argument :code:`sep`. For example, 
    :code:`sep='|'` if your file is delimited by the pipe symbol.
    
    There are many options that may be useful, such as those that parse dates,
    ignore columns, or convert certain values to 'nan's.
    See the pandas documentation for :py:func:`pandas.read_csv` to see all 
    optional arguments.

    Arguments:
        filepath: The path to the file to read

    Keyword Arguments:
        **kwargs: See the pandas documentation for :py:func:`pandas.read_csv`

    Returns:
        A numpy array. This array will be 1D if the csv file contains only a
        single row or column of data. Otherwise the array will be 2D.
    
    """
    df = pandas.read_csv(filepath, *args, **kwargs)
    arr = df.to_numpy()

    # convert array to 1D if it only has one row or column
    if arr.ndim > 1 and 1 in arr.shape:
        return arr.flatten()
    else:
        return arr