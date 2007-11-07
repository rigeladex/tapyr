# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    CTK_Toolbar
#
# Purpose
#    Provide toolbar widget
#
# Revision Dates
#    13-Apr-2000 (CT) Creation
#    28-Jun-2000 (CT) `index' and `delta' added to `add_category'
#    28-Jun-2000 (CT) `_repack' and `_repack_1' added
#    28-Sep-2004 (CT) Use `isinstance` instead of type comparison
#     8-Apr-2005 (CT) `apply` and `string`-method calls removed
#     7-Nov-2007 (CT) Moved into package _TFL._TKT._Tk
#    ««revision-date»»···
#--

from _TFL._TKT._Tk.CT_TK   import *
from _TFL.NO_List          import NO_List

class Toolbar (C_Frame) :
    """Toolbar widget"""

    widget_class = "Toolbar"

    def __init__ ( self, master
                 , name          = None
                 , help          = None
                 , balloon       = None
                 , ** kw
                 ) :
        C_Frame.__init__ (self, master, name, self.widget_class, ** kw)
        self.categories = NO_List ()
        self.help       = help
        self.balloon    = balloon
        self.__pending  = None
    # end def __init__

    def add_category (self, name, index = None, delta = 0, ** kw) :
        """Add a Buttongrid widget for category `name' to toolbar"""
        if isinstance (index, str) :
            index = index.lower ()
        self._set_options      \
            ( kw
            , relief      = RAISED
            , borderwidth = 2
            , help        = self.help
            , balloon     = self.balloon
            )
        tb_cat = Buttongrid    (self, name.lower (), ** kw)
        self.categories.insert (index, tb_cat, delta)
        self._repack           ()
        return tb_cat
    # end def add_category

    def add_button (self, category, name, ** kw) :
        """Add a button with `name' to `category'. `kw' is passed to the
           constructor of `C_Button'
        """
        if not isinstance (category, Buttongrid) :
            category = self [category]
        self._set_options \
            ( kw
            , relief      = FLAT
            , borderwidth = 0
            )
        return category.add (name, ** kw)
    # end def add_button

    def __getitem__ (self, index) :
        if isinstance (index, str) :
            index = index.lower ()
        return self.categories [index]
    # end def __getitem__

    def _repack (self) :
        if not self.__pending :
            self.__pending = self.after_idle (self._repack_1)
    # end def _repack

    def _repack_1 (self, event = None) :
        for c in self.categories :
            c.pack_forget ()
        for c in self.categories :
            c.pack (side = LEFT, padx = 1, pady = 1)
        self.__pending = None
    # end def _repack_1

# end class Toolbar

### __END__ TFL.TKT.Tk.CTK_Toolbar
