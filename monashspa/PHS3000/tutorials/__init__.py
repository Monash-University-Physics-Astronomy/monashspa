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

# Advanced fitting tutorial data
from . import fitting

from ..optical_tweezers import trap_k_theory as __trap_k_theory

def model_1(r, w, I):
    # scale parameters
    r = r*1e-3
    w = w*1e-4
    I = I*1e11
    
    # set parameters we are not exposing
    eccentricity = 1.1
    alpha = 1.25

    return __trap_k_theory(r, w, alpha, eccentricity, I)