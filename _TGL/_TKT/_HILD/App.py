# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.HILD.App
#
# Purpose
#    Wrapper for the hildon widget App (Nokia 770 gtk+ extensions)
#
# Revision Dates
#    21-Jan-2006 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._HILD         import HILD
from   _TGL._TKT._GTK          import GTK
import _TGL._TKT._HILD.App_View
import _TGL._TKT._HILD.Window

class App (HILD.Window) :
    """Wrapper for the hildon widget App"""

    GTK_Class        = HILD.hildon.App
    __gtk_properties = \
        ( ### title has the same effekt GTK.Property            ("app_title")
          GTK.SG_Object_Property
            ( "view"
            , get_fct_name = "get_appview"
            , set_fct_name = "set_appview"
            )
        , GTK.Property            ("killable")
        , GTK.Property            ("scroll_control")
        , GTK.SG_Property         ("two_part_title")
        , GTK.Property            ("zoom")
        )

    def __init__ (self, view = None, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        if view is None :
            view  = self.TNS.App_View (title = None, AC = self.AC)
        self.view = view
    # end def __init__

# end class App

if __name__ != "__main__" :
    HILD._Export ("App")
### __END__ TGL.TKT.HILD.App
