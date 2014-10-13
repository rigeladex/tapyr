# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SWP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.SWP.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    16-Feb-2010 (MG) Creation (based on GTW.OMP.PAP.Nav)
#    24-Feb-2010 (CT) Creation continued
#    11-Mar-2010 (MG) Special widget's used for event date/time
#    23-Mar-2010 (CT) `Gallery` and `Picture` added
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#     7-Nov-2011 (CT) Remove boilerplate from `afs_spec` for Entity_Link `clips`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Remove `Form_args`, `*_completer`,
#                     i.e., stuff related to non-AFS forms
#    28-Jan-2014 (CT) Add `Referral`
#    26-Aug-2014 (CT) Replace `GTW.AFS` specification by `MF3_Form_Spec`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Clip_X               = dict \
        ( ETM            = "GTW.OMP.SWP.Clip_X"
        , list_display   =
            ( "ui_display", "short_title", "date", "created_by", "format"
            , "last_changed"
            )
        , sort_key       = TFL.Sorted_By ("-date.start", "-prio", "perma_name")
        )

    Gallery              = dict \
        ( ETM            = "GTW.OMP.SWP.Gallery"
        , sort_key       = TFL.Sorted_By ("-date.start", "perma_name")
        )

    Page                 = dict \
        ( ETM            = "GTW.OMP.SWP.Page"
        , list_display   =
            ( "ui_display", "short_title", "date", "created_by", "format"
            , "last_changed"
            )
        , sort_key       = TFL.Sorted_By ("-date.start", "-prio", "perma_name")
        , MF3_Attr_Spec        = dict
            ( { "events.recurrence"    : dict
                ( include_rev_refs     = ("rules", )
                )
              }
            , events           = dict
                ( include_rev_refs = ("recurrence", )
                )
            )
        , MF3_Form_Spec        = dict
            ( include_rev_refs = ("events", "clips")
            )
        )

    Picture              = dict \
        ( ETM            = "GTW.OMP.SWP.Picture"
        , sort_key       = TFL.Sorted_By \
            ("-left.date.start", "left.perma_name", "number")
        )

    Referral             = dict \
        ( ETM            = "GTW.OMP.SWP.Referral"
        , list_display   = \
            ("date", "parent_url", "perma_name", "short_title")
        , sort_key       = TFL.Sorted_By \
            ("-date.start", "parent_url", "perma_name")
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.SWP._Export_Module ()
### __END__ GTW.OMP.SWP.Nav
