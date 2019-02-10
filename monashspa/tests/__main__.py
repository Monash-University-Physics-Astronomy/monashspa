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

if __name__ == "__main__":
    # print python version
    import sys
    print("Python version:", sys.version)
    # print monashspa version
    import monashspa
    print("monashspa version:", monashspa.__version__)
    # print numpy version
    import numpy
    print("numpy version:", numpy.__version__)
    # print matplotlib version
    import matplotlib
    print("matplotlib version:", matplotlib.__version__)
    # print lmfit version
    import lmfit
    print("lmfit version:", lmfit.__version__)

    print()
    print("Running tests now...")
    
    failed_tests = []
    
    from . import fitting
    failed_tests.extend(fitting.do_tests())

    from .PHS3000 import optical_tweezers
    failed_tests.extend(optical_tweezers.do_tests())

    print()
    print("Tests complete.")
    if failed_tests:
        print("Error: There were {} failed tests".format(len(failed_tests)))
    else:
        print("All tests completed successfully!")