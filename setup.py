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

# Define the current version of the library
# Update this before building and publishing a new version
# see https://semver.org/ for guidelines on how to modify the version string
VERSION = '0.7.0'

# get directory of setup.py and the rest of the code for the library
code_dir = os.path.abspath(os.path.dirname(__file__))

# Auto generate a __version__ file for the package to import
with open(os.path.join(code_dir, 'monashspa', '__version__.py'), 'w') as f:
    f.write("__version__ = '%s'\n" % VERSION)

# Work around the fact that the readme.md file doesn't exist for users installing
# from the tar.gz format. However, in this case, they won't be uploading to PyPi
# so they don't need it!
try:
    # Read in the readme file as the long description
    with open(os.path.join(code_dir, 'readme.md')) as f:
        long_description = f.read()
except Exception:
    long_description = ""

setup(
    name='monashspa',
    version=VERSION,
    description='Library of useful data analysis tools for Monash University Physics & Astronomy students',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://monashspa.readthedocs.io',
    project_urls={
        "Documentation": "https://monashspa.readthedocs.io",
        "Source Code": "https://bitbucket.org/monashuniversityphysics/monashspa",
    },
    license='GPLv3',
    author='School of Physics & Astronomy, Monash University',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
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
        'requests>=2.21.0,<3',
        'colorama>=0.4.1,<1',
        'pandas>=0.22,<1',
        'six',
        'piradon',
    ],
    data_files=[
        ('monashspa/PHS2061', ['monashspa/PHS2061/PHS20x1UncertaintiesData.csv']),
    ]
)