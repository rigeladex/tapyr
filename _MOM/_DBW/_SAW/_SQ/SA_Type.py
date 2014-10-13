# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.SQ.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.SQ.SA_Type
#
# Purpose
#    Encapsulate SQLalchemy types for SQLite
#
# Revision Dates
#    18-Jul-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

from   _MOM._DBW._SAW        import SA
import _MOM._DBW._SAW.SA_Type

class _SQ_SA_Type_ (MOM.DBW.SAW.SA_Type) :
    """Encapsulate SQLalchemy types for SQLite"""

    _real_name   = "SA_Type"

SA_Type = _SQ_SA_Type_ # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.SQ._Export ("SA_Type")
### __END__ MOM.DBW.SAW.SQ.SA_Type
