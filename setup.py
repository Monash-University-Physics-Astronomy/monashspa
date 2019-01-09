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
from setuptools import setup, find_packages


VERSION = '0.1.0'
# Auto generate a __version__ package for the package to import
with open(os.path.join('monashspa', '__version__.py'), 'w') as f:
    f.write("__version__ = '%s'\n" % VERSION)

setup(
    name='monashspa',
    version=VERSION,
    description='Library of useful data analysis tools for Monash University Physics & Astronomy students',
    url='https://bitbucket.org/monashuniversityphysics/monashspa',
    license='GPLv3',
    author='School of Physics & Astronomy, Monash University',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Environment :: Console',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Natural Language :: English',
                ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'lmfit>=0.9.12,<1.0',
    ],
)