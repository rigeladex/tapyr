# -*- coding: utf-8 -*-
# Copyright (C) 2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package GTW.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.__init__
#
# Purpose
#    Support for web forms
#
# Revision Dates
#    18-Jan-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

Form       = Package_Namespace ()
Form.BREAK = False ### used for debugging

GTW._Export ("Form")

del Package_Namespace

### __END__ GTW.Form.__init__
