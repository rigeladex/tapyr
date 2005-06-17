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
#     3-Apr-2005 (MG) First style properties added
#     5-Apr-2005 (MG) `Color_Property` added and used for `foreground` and
#                     `background`
#     5-Apr-2005 (MG) Old style porperties removed
#    13-May-2005 (MG) `toplevel` added
#    13-May-2005 (MG) `Color_Property` moved from `_wtk_delegation` to
#                     `__gtk_properties`
#    15-May-2005 (MG) `add_accelerator` added
#    16-May-2005 (MG) `create_pango_layout` added
#    18-May-2005 (MG) `exposed_widget` added
#    20-May-2005 (MG) `__init__`: call to `read_widget_memory` added
#    20-May-2005 (MG) `grab_*` added
#     3-Jun-2005 (MG) `destroy` added
#    17-Jun-2005 (MG) `colormap` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object

class Color_Property (GTK.SG_Property) :
    """A property which set's and get's a color of a widget."""

    def __init__ (self, name, set_fct) :
        self.__super.__init__ (name, get = self._get, set = self._set)
        self._attr_name    = "_%s" % (name, )
        self._set_fct_name = set_fct
    # end def __init__

    def _get (self, obj) :
        return getattr (obj, self._attr_name, None)
    # end def _get

    def _set (self, obj, value) :
        setattr (obj, self._attr_name, value)
        if value :
            value = GTK.gtk.gdk.color_parse (value)
        getattr (obj.wtk_object, self._set_fct_name) \
            (GTK.gtk.STATE_NORMAL, value)
    # end def _set

# end class Color_Property

class Widget (GTK.Object) :
    """Base class for all real GTK widgets"""

    GTK_Class        = GTK.gtk.Widget
    __gtk_properties = \
        ( GTK.Property           ("app_paintable")
        , GTK.Property           ("can_default")
        , GTK.Property           ("can_focus")
        , GTK.SG_Property        ("colormap", set = None)
        , GTK.Property           ("composite_child", set = None)
        , GTK.SG_Property        ("events")
        , GTK.SG_Property        ("extension_events")
        , GTK.Property           ("has_default")
        , GTK.Property           ("has_focus")
        , GTK.Property           ("height_request")
        , GTK.Property           ("is_focus")
        , GTK.SG_Property        ("name")
        , GTK.SG_Property        ("no_show_all")
        , GTK.SG_Property        ("parent")
        , GTK.Property           ("receives_default")
        , GTK.Property           ("sensitive")
        , GTK.SG_Property        ("style")
        , GTK.Property           ("visible")
        , GTK.SG_Object_Property ("toplevel", set = False)
        , GTK.Property           ("width_request")
        , Color_Property         ("background", "modify_bg")
        , Color_Property         ("foreground", "modify_fg")
        )

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator          ("show")
        , GTK.Delegator          ("hide")
        , GTK.Delegator          ("show_all")
        , GTK.Delegator          ("hide_all")
        , GTK.Delegator          ("create_pango_layout")
        , GTK.Delegator_2O       ("add_accelerator")
        , GTK.Delegator          ("grab_add")
        , GTK.Delegator          ("grab_remove")
        , GTK.Delegator          ("destroy")
        )

    exposed_widget = property (lambda s : s)

    def __init__ (self, * args, ** kw) :
        name = None
        if "name" in kw :
            name = kw ["name"]
            del kw    ["name"]
        self.__super.__init__ (* args, ** kw)
        if name is not None :
            self.name         = name
            self.read_widget_memory ()
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
    GTK._Export ("Widget", "Color_Property")
### __END__ TGL.TKT.GTK.Widget
