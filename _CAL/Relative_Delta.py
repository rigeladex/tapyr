# -*- coding: utf-8 -*-
# Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CAL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CAL.Relative_Delta
#
# Purpose
#    Wrapper around `dateutil.relativedelta.relativedelta`
#
# Revision Dates
#     2-Feb-2016 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _CAL                       import CAL
from   _TFL                       import TFL

import _CAL.Date
import _CAL.Date_Time

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

import datetime

class Relative_Delta (TFL.Meta.Object) :
    """Relative delta based on `dateutil.relativedelta`"""

    _OP = TFL.Meta.Class_and_Instance_Once_Property
    MO  = _OP (lambda soc : soc.RD.MO)
    TU  = _OP (lambda soc : soc.RD.TU)
    WE  = _OP (lambda soc : soc.RD.WE)
    TH  = _OP (lambda soc : soc.RD.TH)
    FR  = _OP (lambda soc : soc.RD.FR)
    SA  = _OP (lambda soc : soc.RD.SA)
    SU  = _OP (lambda soc : soc.RD.SU)

    def __init__ (self, ** kw) :
        self._kw = kw
    # end def __init__

    @TFL.Meta.Class_and_Instance_Once_Property
    def RD (soc) :
        from dateutil import relativedelta
        return relativedelta
    # end def RD

    @TFL.Meta.Once_Property
    def _body (self) :
        return self.RD.relativedelta (** self._kw)
    # end def _body

    def dt_op (self, dot, op) :
        result = op (dot._body, self._body)
        return dot.new_dtw (result)
    # end def dt_op

# end class Relative_Delta

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ CAL.Relative_Delta
