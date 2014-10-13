# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.EVT.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.EVT.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    15-Mar-2010 (CT) Creation
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     8-Nov-2011 (CT) `Calendar` added
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Remove `Form_args`,
#                     i.e., stuff related to non-AFS forms
#    24-Feb-2012 (CT) Remove `Event_occurs` (too electric by far)
#    24-Feb-2014 (CT) Change `Event.list_display` (add `short_title`; order)
#    26-Aug-2014 (CT) Replace `GTW.AFS` specification by `MF3_Form_Spec`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Calendar            = dict \
        ( ETM           = "GTW.OMP.EVT.Calendar"
        )
    Event               = dict \
        ( ETM           = "GTW.OMP.EVT.Event"
        , list_display  = ("date", "time", "short_title", "left", "calendar")
        , sort_key      = TFL.Sorted_By
            ("-date.start", "-time.start", "short_title", "left")
        , MF3_Attr_Spec        = dict
            ( recurrence       = dict
                ( include_rev_refs = ("rules", )
                )
            )
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("recurrence", )
            )
        )
    Recurrence_Spec     = dict \
        ( ETM           = "GTW.OMP.EVT.Recurrence_Spec"
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("rules", )
            )
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.EVT._Export_Module ()
### __END__ GTW.OMP.EVT.Nav
