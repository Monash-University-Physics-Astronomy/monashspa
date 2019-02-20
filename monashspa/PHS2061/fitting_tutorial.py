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
import pandas

try:
    __filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PHS20x1UncertaintiesData.csv')
    data = pandas.read_csv(__filepath, usecols=[0,1,2])
    data = data.to_numpy()
except:
    data = "Warning: failed to import data from csv file. Possibly the monashspa library is not installed correctly."