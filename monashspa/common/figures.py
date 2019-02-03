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

import matplotlib.pyplot as plt
from matplotlib.legend import Legend as mplLegend

def savefig(fname, dpi=600, bbox_inches='tight', **kwargs):
    """ A wrapper for :py:func:`matplotlib.pyplot.savefig` with sensible defaults.
    
    By default, if a matplotlib legend is located outside of the plot axes,
    then :py:func:`matplotlib.pyplot.savefig` may cut off the legend when saving the
    figure. This function fixes this issue by setting :code:`bbox_inches='tight'`
    and setting :code:`bbox_extra_artists` to be a list of the current figure legends,
    unless the user chooses to define them otherwise. This function also sets 
    the default for :code:`dpi` to 600, which is large enough for most purposes.

    This function accepts any keyword argument from :py:func:`matplotlib.pyplot.savefig`
    and returns the result of the call to that function. 
    See :py:func:`matplotlib.pyplot.savefig` for usage.
    """
    
    if 'bbox_extra_artists' not in kwargs:
        ax = plt.gca()
        kwargs['bbox_extra_artists'] = [c for c in ax.get_children() if isinstance(c, mplLegend)]
    
    return plt.savefig(fname, dpi=dpi, bbox_inches=bbox_inches, **kwargs)