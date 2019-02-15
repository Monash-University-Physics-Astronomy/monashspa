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

#: Resistance data for temperatures below 77K as a 2D numpy array.
#: Columns are: temperature (K), u_temperature (K), resistance (Ohms),
#: u_resistance(Ohms) respectively
liquid_helium = np.array([
    (76.9, 0.1, 37,   1),
    (67.0, 0.1, 32,   1),
    (61.5, 0.1, 30,   1),
    (57.0, 0.1, 29,   1),
    (51.9, 0.1, 27,   1),
    (47.0, 0.1, 26,   1),
    (42.0, 0.1, 26,   1),
    (38.0, 0.1, 26,   1),
    (31.9, 0.1, 28,   1),
    (26.8, 0.1, 31,   1),
    (21.9, 0.1, 39,   1),
    (20.0, 0.1, 46,   1),
    (18.1, 0.1, 53,   1),
    (16.0, 0.1, 65,   1),
    (13.8, 0.1, 106,  1),
    (12.0, 0.1, 162,  1),
    (10.0, 0.1, 526,  1),
    (8.0,  0.1, 3.23, 0.01e3),
    (6.0,  0.1, 292,  1e3),
    (4.0,  0.1, 81.7, 0.1e6),
])
