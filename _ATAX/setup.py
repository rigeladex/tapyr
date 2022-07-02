#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016-2020 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# Web: https://www.gg32.com/en/ Email: tanzer@swing.co.at
# All rights reserved
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    _ATAX.setup
#
# Purpose
#    Setup file for package namespace ATAX
#
# Revision Dates
#    11-Oct-2016 (CT) Creation
#    13-Oct-2016 (CT) Use `find_packages`, `_TFL.fs_find`, not home-grown code
#    22-Feb-2017 (CT) Use `TFL_STP`, not home-grown code
#    27-Feb-2017 (CT) Add Python 3.6 to `classifiers`
#    25-Mar-2020 (CT) Restrict Python versions to >=3.7
#    ««revision-date»»···
#--

from   setuptools               import setup

import TFL_STP as STP

STP.change_to_dir (__file__)

license = "BSD License"
name    = "ATAX"
p_name  = "_ATAX"

version              = STP.package_version ()
long_description     = STP.long_description ()
packages, data_files = STP.packages_plus_data_files (p_name)
Test_Command         = STP.Test_Command

if __name__ == "__main__" :
    setup \
    ( name                 = name
    , version              = version
    , description          =
        "Package for doing Einnahmen-Ausgabenrechnung according to "
        "Austrian tax laws."
    , long_description     = long_description
    , license              = license
    , author               = "Christian Tanzer"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://codeberg.org/tanzer/tapyr"
    , packages             = packages
    , package_dir          = { p_name : "." }
    , package_data         = { p_name : data_files }
    , platforms            = "Any"
    , classifiers          = \
        [ "Development Status :: 5 - Production/Stable"
        , "License :: OSI Approved :: " + license
        , "Operating System :: OS Independent"
        , "Programming Language :: Python"
        , "Topic :: Office/Business :: Financial :: Accounting"
        ]
    , python_requires      = ">=3.7"
    , setup_requires       = ["TFL_STP>=3"]
    , install_requires     = ["TFL>=3", "CAL>=3"]
    , extras_require       = dict ()
    , cmdclass             = dict (test = Test_Command)
    , zip_safe             = False ### no eggs, please
    )

### __END__ _ATAX.setup
