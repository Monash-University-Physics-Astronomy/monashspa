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

def read_mca_file(filepath):
    """Imports data saved from the ADMCA software

    Arguments:
        filepath: The path to the .mca file produced by the ADMCA
                  acquisition software

    Returns:
        A tuple :code:`(header, data)` where :code:`header` is a dictionary
        containing the key, value pairs from header rows of the .mca file and
        :code:`data` is a 1D numpy array of the counts for each MCA channel.

    """

    header = {}
    data = []
    reading_header = False
    reading_data = False
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip('\r\n')
            if line == '<<PMCA SPECTRUM>>':
                reading_header = True
                continue
            elif line == '<<DATA>>':
                reading_header = False
                reading_data = True
                continue
            elif line == '<<END>>':
                break
            elif reading_header:
                try:
                    key, value = line.split(' - ')
                    header[key] = value
                except Exception:
                    pass
            elif reading_data:
                data.append(int(line))
    return header, np.array(data)
