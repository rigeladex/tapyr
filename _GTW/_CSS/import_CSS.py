# -*- coding: utf-8 -*-
# Copyright (C) 2011-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.CSS.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.CSS.import_CSS
#
# Purpose
#    Import all CSS classes necessary to define CSS fragments
#
#    Usage::
#
#        from _GTW._CSS.import_CSS import *
#
# Revision Dates
#     1-Jan-2011 (CT) Creation
#    21-Feb-2011 (CT) `Border` added
#    17-Jan-2012 (CT) Import `GTW.CSS.Color` instead of `TFL.Color`
#    12-Apr-2014 (CT) Import `Property`, not `Border`
#    ««revision-date»»···
#--

from _GTW._CSS             import Media
from _GTW._CSS.Color       import *
from _GTW._CSS.Length      import *
from _GTW._CSS.Property    import *
from _GTW._CSS.Rule        import *
from _GTW._CSS.Style_Sheet import *

### __END__ GTW.CSS.import_CSS
