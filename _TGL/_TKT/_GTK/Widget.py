# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Widget
#
# Purpose
#    Base class for all GTK widgets
#
# Revision Dates
#    21-Mar-2005 (MG) Creation
#    26-Mar-2005 (MG) `_wtk_delegation` and `__init__` added
#    31-Mar-2005 (MG) Key binding and new button signals added
#     1-Apr-2005 (MG) `_wtk_delegation` changed
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object

class Widget (GTK.Object) :
    """Base class for all real GTK widgets"""

    GTK_Class        = GTK.gtk.Widget
    __gtk_properties = \
        ( GTK.Property     ("app_paintable")
        , GTK.Property     ("can_default")
        , GTK.Property     ("can_focus")
        , GTK.Property     ("composite_child", set = None)
        , GTK.SG_Property  ("events")
        , GTK.SG_Property  ("extension_events")
        , GTK.Property     ("has_default")
        , GTK.Property     ("has_focus")
        , GTK.Property     ("height_request")
        , GTK.Property     ("is_focus")
        , GTK.SG_Property  ("name")
        , GTK.SG_Property  ("no_show_all")
        , GTK.SG_Property  ("parent")
        , GTK.Property     ("receives_default")
        , GTK.Property     ("sensitive")
        , GTK.SG_Property  ("style")
        , GTK.Property     ("visible")
        , GTK.Property     ("width_request")
        )

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator ("show")
        , GTK.Delegator ("hide")
        , GTK.Delegator ("show_all")
        , GTK.Delegator ("hide_all")
        )

    def __init__ (self, * args, ** kw) :
        name = None
        if "name" in kw :
            name = kw ["name"]
            del kw    ["name"]
        self.__super.__init__ (* args, ** kw)
        if name :
            self.name         = name
        self._key_bindings    = {}
        self._button_bindings = {}
    # end def __init__

# end class Widget

import gobject
gobject.signal_new \
    ( "key-binding", GTK.gtk.Widget, gobject.SIGNAL_ACTION
    , bool, (int, )
    )
for kind in "single", "double", "triple" :
    for number in 1, 2, 3 :
        event = "%s-click-%d-event" % (kind, number)
        gobject.signal_new \
            (event, GTK.gtk.Widget, gobject.SIGNAL_RUN_LAST, bool, (object, ))

if __name__ != "__main__" :
    GTK._Export ("Widget")
### __END__ TGL.TKT.GTK.Widget
