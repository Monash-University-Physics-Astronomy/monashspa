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

import numpy as np

#: The calibration data for wavemeter #4929 as a 2D numpy array.
#: Here the first column corresponds to wavemeter reading in mm
#: and the second column corresponds to the frequency in GHz.
wavemeter_calibration = np.array([
    (24.215, 7.702),
    (22.675, 7.8),
    (21.255, 7.9),
    (19.97,  8.0),
    (18.81,  8.1),
    (17.75,  8.2),
    (16.79,  8.3),
    (15.91,  8.4),
    (15.06,  8.5),
    (14.36,  8.6),
    (13.64,  8.7),
    (12.98,  8.8),
    (12.35,  8.9),
    (11.77,  9.0),
    (11.21,  9.1),
    (10.69,  9.2),
    (10.20,  9.3),
    (9.73,   9.4),
    (9.29,   9.5),
    (8.87,   9.6),
    (8.46,   9.7),
    (8.08,   9.8),
    (7.71,   9.9),
    (7.36,   10.0),
    (7.03,   10.1),
    (6.71,   10.2),
    (6.39,   10.3),
    (6.09,   10.4),
    (5.81,   10.5),
    (5.52,   10.6),
    (5.26,   10.7),
    (5.00,   10.8),
    (4.75,   10.9),
    (4.50,   11.0),
    (4.28,   11.1),
    (4.06,   11.2),
    (3.84,   11.3),
    (3.62,   11.4),
    (3.42,   11.5),
    (3.22,   11.6),
    (3.03,   11.7),
    (2.85,   11.8),
    (2.66,   11.9),
    (2.49,   12.0),
])