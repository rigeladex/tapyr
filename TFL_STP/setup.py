# -*- coding: utf-8 -*-
# Copyright (C) 2017-2023 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package TFL_STP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL_STP.setup
#
# Purpose
#    Setup file for package TFL_STP
#
# Revision Dates
#    23-Feb-2017 (CT) Creation
#    27-Feb-2017 (CT) Add Python 3.6 to `classifiers`
#    25-Mar-2020 (CT) Restrict Python versions to >=3.7
#    29-May-2023 (CT) Restrict Python versions to >=3.8
#    ««revision-date»»···
#--

from   codecs      import open
from   setuptools  import setup
import os

src_dir = os.path.dirname (__file__)
if src_dir :
    os.chdir (src_dir)

license = "BSD License"
name    = "TFL_STP"
p_name  = "TFL_STP"

long_description = open ("README.rst", encoding = "utf-8").read ().strip ()
packages         = [ p_name ]
data_files       = ["LICENSE", "README.rst", "setup.py", "setup.cfg"]

if __name__ == "__main__" :
    setup \
    ( name                 = name
    , version              = "3.0"
    , description          = "Setup helper functions for TFL-based packages"
    , long_description     = long_description
    , license              = license
    , author               = "Christian Tanzer"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://codeberg.org/tanzer/tapyr"
    , packages             = packages
    , package_dir          = { p_name : "." }
    , package_data         = { p_name : data_files }
    , platforms            = "Any"
    , include_package_data = True
    , classifiers          = \
        [ "Development Status :: 5 - Production/Stable"
        , "License :: OSI Approved :: " + license
        , "Operating System :: OS Independent"
        , "Programming Language :: Python"
        , "Intended Audience :: Developers"
        , "Topic :: Software Development :: Libraries :: Python Modules"
        ]
    , python_requires      = ">=3.8"
    , setup_requires       = []
    , install_requires     = []
    , zip_safe             = False ### no eggs, please
    )

### __END__ TFL_STP.setup
