# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.EVT.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.EVT.graph
#
# Purpose
#    Graph describing EVT (partial) object model
#
# Revision Dates
#    24-Sep-2012 (CT) Creation
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _GTW._OMP._SRM

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip

import _MOM._Graph.Command
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD
from   _TFL.I18N              import _, _T

def graph (app_type) :
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.EVT.Event
            ( Role.left     (offset = CD.W)
            , Attr.calendar (offset = CD.N)
            , ET.EVT.Recurrence_Spec
                ( ET.EVT.Recurrence_Rule (offset = CD.E)
                , offset = CD.E
                )
            )
        , desc  = _T ("Graph displaying EVT partial object model")
        , title = _T ("EVT graph")
        )
# end def graph

class Command (MOM.Graph.Command) :

    @property
    def PNS (self) :
        return GTW.OMP.EVT
    # end def PNS

# end class Command

if __name__ != "__main__" :
    GTW.OMP.EVT._Export ("*")
else :
    import _GTW._OMP._EVT.import_EVT
    import _GTW._OMP._SWP.import_SWP
    Command () ()
### __END__ GTW.OMP.EVT.graph
