# -*- coding: utf-8 -*-
# Copyright (C) 2004-2016 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    run_doctest
#
# Purpose
#    Run doctest on all modules specified on command line
#
# Revision Dates
#    10-Oct-2016 (CT) Use `TFL.run_doctest`
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL.run_doctest

if __name__ == "__main__" :
    TFL.run_doctest.Command ()
### __END__ run_doctest
