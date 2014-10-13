# -*- coding: utf-8 -*-
# Copyright (C) 2005-2007 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Text_View
#
# Purpose
#    Wrapper for the GTK widget TextView
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#     2-Apr-2005 (MG) `__init__` added
#     5-Apr-2005 (MG) `Styler` and `background` property added
#    14-Dec-2007 (MG) Import fixed
#    ««revision-date»»···
#--

from   _TFL.predicate            import dict_from_list
from   _TGL                      import TGL
import _TGL._TKT._GTK.Container
import _TGL._TKT._GTK.Styler
import _TGL._TKT._GTK.Text_Buffer

GTK = TGL.TKT.GTK

class Text_View (GTK.Container) :
    """Wrapper for the GTK widget TextView"""

    class Styler (TGL.TKT.GTK.Styler) :
        Opts    = dict_from_list (("background", ))
    # end class Styler

    GTK_Class        = GTK.gtk.TextView
    __gtk_properties = \
        ( GTK.SG_Property         ("accepts_tab")
        , GTK.SG_Object_Property  ("buffer")
        , GTK.SG_Property         ("cursor_visible")
        , GTK.SG_Property         ("editable")
        , GTK.SG_Property         ("indent")
        , GTK.SG_Property         ("justification")
        , GTK.SG_Property         ("left_margin")
        , GTK.SG_Property         ("overwrite")
        , GTK.SG_Property         ("pixels_above_lines")
        , GTK.SG_Property         ("pixels_below_lines")
        , GTK.SG_Property         ("pixels_inside_wrap")
        , GTK.SG_Property         ("right_margin")
        , GTK.SG_Property         ("tabs")
        , GTK.SG_Property         ("wrap_mode")
        , GTK.Color_Property      ("background", "modify_base")
        )

    def __init__ (self, AC = None, ** kw) :
        if buffer not in kw :
            kw ["buffer"] = GTK.Text_Buffer (AC = AC)
        ### we need the `_buffer` reference to prevent that the garbage
        ### collector destroys the `Text_Buffer`
        self._buffer      = b = kw ["buffer"]
        kw ["buffer"]     = b.wtk_object
        self.__super.__init__ (** kw)
    # end def __init__

# end class Text_View

if __name__ != "__main__" :
    GTK._Export ("Text_View")
### __END__ TGL.TKT.GTK.Text_View
