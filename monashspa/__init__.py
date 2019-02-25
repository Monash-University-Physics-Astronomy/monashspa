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

from __future__ import print_function
try:
    from .__version__ import __version__
except ImportError:
    # Version file has not been autogenerated from build process:
    __version__ = 'Unknown development version'

def __colorise(enable, text):
    if enable:
        text = "\033[31;1m" +text+ "\033[0m"
    return text

def __check_for_new_monashspa_version():
    upgrade = False
    colorama_enabled = False
    try:
        import colorama
        colorama.init(strip=False)
        colorama_enabled = True
    except Exception:
        pass
    
    try:
        import requests
        # hack to work around the fact that sometimes the first attempt to 
        # reach PyPi times out (or takes much longer than it should), 
        # especially when the library is being imported for the first time 
        # in a while. Subsequent restarts of Python and importing don't
        # result in the bug occurring.
        # This might be a bug with the requests library, or it could be
        # something to do with DNS queries...not 100% sure.
        # Either way, initial testing indicates this works reasonably well.
        #
        # This code tries twice if it has to, raises the exception (to be
        # caught by the outer block) if it fails twice, and only checks once
        # if it succeeds first try.
        for i in range(2):
            try:
                r = requests.get('https://pypi.python.org/pypi/monashspa/json', timeout=0.1)
            except requests.exceptions.ReadTimeout:
                if i == 1:
                    raise
            else:
                if i == 0:
                    break
        
        # Get the latest version from PyPi
        online_version = r.json()['info']['version']
        if online_version != __version__:
            # check to see if version is newer
            o_major, o_minor, o_patch = online_version.split('.')
            try:
                l_major, l_minor, l_patch = __version__.split('.')
            except Exception:
                upgrade = True
            else:
                if int(l_major) < int(o_major):
                    upgrade = True
                elif int(l_major) == int(o_major) and int(l_minor) < int(o_minor):
                    upgrade = True
                elif int(l_major) == int(o_major) and int(l_minor) == int(o_minor) and int(l_patch) < int(o_patch):
                    upgrade = True
            
            if upgrade:
                print(__colorise(colorama_enabled, "[monashspa:info] A new version of monashspa is available"))
                print(__colorise(colorama_enabled, "[monashspa:info] You are running monashspa version: {}".format(__version__)))
                print(__colorise(colorama_enabled, "[monashspa:info] The latest monashspa version is: {}".format(online_version)))
                print(__colorise(colorama_enabled, "[monashspa:info] To upgrade, run: "))
                print(__colorise(colorama_enabled, "[monashspa:info]     pip install -U monashspa"))
                print(__colorise(colorama_enabled, "[monashspa:info] from a terminal or Anaconda Prompt (or see the install instructions at https://monashspa.readthedocs.io)"))
                print(__colorise(colorama_enabled, "[monashspa:info] You will need to restart your open Python/IPython/Spyder application after upgrading to use the new version."))
        
    except Exception:
        print(__colorise(colorama_enabled, "[monashspa:info] Unable to check if a newer version is available"))
        print(__colorise(colorama_enabled, "[monashspa:info] You are running monashspa version: {}".format(__version__)))
        print(__colorise(colorama_enabled, "[monashspa:info] You can find the latest version number at: https://monashspa.readthedocs.io"))
    
    try:
        colorama.deinit()
    except Exception:
        pass

    return upgrade

__check_for_new_monashspa_version()