#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL
#
# Purpose
#    Main program for Pythonic Calendaer Application
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _CAL import CAL
import _CAL._UI.Starter

def main () :
    cmd = CAL.UI.Starter.command_spec ()
    CAL.UI.Starter (CAL, cmd)
# end def main

if __name__ == "__main__" :
    main ()
### __END__ CAL
