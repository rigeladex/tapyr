# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.NAV.Test.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.Test.Templateer
#
# Purpose
#    A faked templateer for testing
#
# Revision Dates
#    19-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object

from   _GTW                  import GTW
import _GTW._NAV._Test

Context = dict

def render (template, context) :
    return template, context
# end def render

if __name__ != "__main__" :
    GTW.NAV.Test._Export ("*")
### __END__ GTW.NAV.Test.Templateer


