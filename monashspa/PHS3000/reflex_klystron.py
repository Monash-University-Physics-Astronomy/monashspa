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

__attenuator_calibration = np.array([
    (0,  0.412,  0.412,  np.nan),
    (2,  0.248,  0.278,  12.14),
    (4,  0.194,  0.231,  11.75),
    (6,  0.143,  0.198,  11.47),
    (8,  0.109,  0.165,  11.22),
    (10, 0.079,  0.136,  11.02),
    (12, 0.054,  0.115,  10.84),
    (14, 0.030,  0.094,  10.66),
    (16, 0.010,  0.074,  10.50),
    (18, np.nan, 0.054,  10.33),
    (20, np.nan, 0.036,  10.17),
    (25, np.nan, np.nan, 9.87),
    (30, np.nan, np.nan, 9.27),
])

__micrometer_1_attenuation = __attenuator_calibration[:,[0,1]]
#: The calibration data for attenuator #1.
#: Here, the first column corresponds to the attentuation at 9.15GHz in dB
#: and the second column corresponds to the micrometer position in inches
micrometer_1_attenuation = __micrometer_1_attenuation[~np.isnan(__micrometer_1_attenuation[:,1])]

__micrometer_2_and_3_attenuation = __attenuator_calibration[:,[0,2]]
#: The calibration data for attenuator #2 and #3.
#: Here, the first column corresponds to the attentuation at 9.15GHz in dB
#: and the second column corresponds to the micrometer position in inches
micrometer_2_and_3_attenuation = __micrometer_2_and_3_attenuation[~np.isnan(__micrometer_2_and_3_attenuation[:,1])]

__micrometer_7925_attenuation = __attenuator_calibration[:,[0,3]]
#: The calibration data for attenuator #7925.
#: Here, the first column corresponds to the attentuation at 9.15GHz in dB
#: and the second column corresponds to the micrometer position in nm
micrometer_7925_attenuation = __micrometer_7925_attenuation[~np.isnan(__micrometer_7925_attenuation[:,1])]

__wavemeter_calibration = np.array([
    (7.7024, 24.161, 24.768, 24.215),
    (7.800,  22.675, 23.216, 22.675),
    (7.9,    21.175, 21.788, 21.255),
    (8.0,    19.895, 20.52,  19.97),
    (8.1,    18.80,  19.31,  18.81),
    (8.2,    17.75,  18.29,  17.75),
    (8.3,    16.79,  17.32,  16.79),
    (8.4,    15.87,  16.42,  15.91),
    (8.5,    15.05,  15.60,  15.06),
    (8.6,    14.30,  14.83,  14.36),
    (8.7,    13.64,  14.20,  13.64),
    (8.8,    12.92,  13.45,  12.98),
    (8.9,    12.39,  12.83,  12.35),
    (9.0,    11.70,  12.24,  11.77),
    (9.1,    11.15,  11.69,  11.21),
    (9.2,    10.63,  11.17,  10.69),
    (9.3,    10.14,  10.67,  10.20),
    (9.4,    9.66,   10.20,  9.73),
    (9.5,    9.22,   9.75,   9.29),
    (9.6,    8.80,   9.33,   8.87),
    (9.7,    8.46,   8.93,   8.46),
    (9.8,    8.08,   8.55,   8.08),
    (9.9,    7.65,   8.18,   7.71),
    (10.0,   7.31,   7.84,   7.36),
    (10.1,   6.97,   7.50,   7.03),
    (10.2,   6.65,   7.18,   6.71),
    (10.3,   6.33,   6.86,   6.39),
    (10.4,   6.03,   6.57,   6.09),
    (10.5,   5.75,   6.28,   5.81),
    (10.6,   5.47,   6.00,   5.52),
    (10.7,   5.20,   5.73,   5.26),
    (10.8,   4.94,   5.47,   5.00),
    (10.9,   4.69,   5.22,   4.75),
    (11.0,   4.45,   4.98,   4.50),
    (11.1,   4.22,   4.74,   4.28),
    (11.2,   4.00,   4.52,   4.06),
    (11.3,   3.77,   4.29,   3.84),
    (11.4,   3.56,   4.09,   3.62),
    (11.5,   3.37,   3.87,   3.42),
    (11.6,   3.17,   3.69,   3.22),
    (11.7,   2.98,   3.51,   3.03),
    (11.8,   2.80,   3.33,   2.85),
    (11.9,   2.62,   3.14,   2.66),
    (12.0,   2.44,   2.96,   2.49),
])

#: The calibration data for wavemeter S/N 4091 as a numpy array
#: Here, the first column corresponds to the frequency in GHz
#: and the second column corresponds to the wavemeter position
wavemeter_4091 = __wavemeter_calibration[:,[0,1]]

#: The calibration data for wavemeter S/N 4930 as a numpy array
#: Here, the first column corresponds to the frequency in GHz
#: and the second column corresponds to the wavemeter position
wavemeter_4930 = __wavemeter_calibration[:,[0,2]]

#: The calibration data for wavemeter S/N 4929 as a numpy array
#: Here, the first column corresponds to the frequency in GHz
#: and the second column corresponds to the wavemeter position
wavemeter_4929 = __wavemeter_calibration[:,[0,3]]