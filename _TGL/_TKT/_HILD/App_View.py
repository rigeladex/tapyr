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
#    TGL.TKT.HILD.App_View
#
# Purpose
#    Wrapper for the hildon widget AppView (Nokia 770 gtk+ extensions)
#
# Revision Dates
#    21-Jan-2006 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._HILD         import HILD
from   _TGL._TKT._GTK          import GTK
import _TGL._TKT._HILD.Bin
import _TGL._TKT._HILD.V_Box
import _TGL._TKT._HILD.Menu

class App_View (HILD.Bin) :
    """Wrapper for the hildon widget AppView"""

    GTK_Class        = HILD.hildon.AppView
    __gtk_properties = \
        ( GTK.SG_Object_Property  ("connected_adjustment")
        , GTK.SG_Property         ("fullscreen")
        , GTK.SG_Property         ("fullscreen_key_allowed")
        , GTK.SG_Property         ("title")
        )

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        AC = self.AC
        for attr, cls_name in (("menu", "Menu"), ("vbox", "V_Box")) :
            obj = getattr (self.wtk_object, "get_%s" % (attr, )) ()
            cls = getattr (self.TNS, cls_name)
            setattr (self, attr, cls (wtk_object = obj, AC = AC))
    # end def __init__

# end class App_View

if __name__ != "__main__" :
    HILD._Export ("App_View")
### __END__ TGL.TKT.HILD.App_View
