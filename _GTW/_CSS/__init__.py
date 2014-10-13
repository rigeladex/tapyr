# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Mag. Christian Tanzer. All rights reserved
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
#    GTW.CSS.__init__
#
# Purpose
#    Model cascading style sheets
#
# Revision Dates
#    29-Dec-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

CSS = Package_Namespace ()
GTW._Export ("CSS")

del Package_Namespace

### __END__ GTW.CSS.__init__
