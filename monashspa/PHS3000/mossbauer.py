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
import xml.etree.ElementTree as ET

import numpy as np

def read_data(filepath):
    """Imports the acquired spectrum from the Mossbauer data file.

    Arguments:
        filepath: The path to the .ws5 file produced by the muon
                  Mossbauer acquisition software.

    Returns:
        A 1D numpy array containing the data (counts) from the file. 

    """

    tree = ET.parse(filepath)
    root = tree.getroot()

    data = None

    for child in root:
        if child.tag == 'data':
            channels = int(child.attrib['channels'])
            raw_data = child.text
            split_data = raw_data.split('\n')
            split_data = [x for x in split_data if x]
            if len(split_data) != channels:
                raise RuntimeError('The file {filename} may be malformed. The number of channels ({channels}) specified does not match the number of data points found ({len_data}).'.format(filename=os.path.basename(filepath), channels=channels, len_data=len(split_data)))
            int_data = [int(x) for x in split_data]
            data = np.array(int_data)
    
    if data is None:
        raise RuntimeError('Could not locate the data in the file {filename}. Is your data saved in the correct file format?'.format(filename=os.path.basename(filepath)))
    else:
        return data
