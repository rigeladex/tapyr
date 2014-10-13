# -*- coding: utf-8 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    DJO.context_processors
#
# Purpose
#    Define context processors for Django
#
# Revision Dates
#    11-Jul-2008 (CT) Creation
#    ««revision-date»»···
#--

from   _DJO            import DJO
import _DJO._NAV.Base

def navigation_root (request) :
    return dict (NAV = DJO.NAV.Root.top)
# end def navigation_root

if __name__ != "__main__" :
    DJO._Export_Module ()
### __END__ context_processors
