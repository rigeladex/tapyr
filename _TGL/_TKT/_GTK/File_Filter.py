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
#    TGL.TKT.GTK.File_Filter
#
# Purpose
#    Wrapper for the GTK widget FileFilter
#
# Revision Dates
#    03-Jun-2005 (MG) Automated creation
#    14-Aug-2005 (MG) `add_pattern` improved
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object

class File_Filter (GTK.Object) :
    """Wrapper for the GTK widget FileFilter"""

    GTK_Class        = GTK.gtk.FileFilter
    __gtk_properties = \
        (
        )

    def __init__ (self, name = None, * patterns, ** kw) :
        self.__super.__init__ (** kw)
        if name :
            self.wtk_object.set_name (name)
        self.add_pattern (* patterns)
    # end def __init__

    def add_pattern (self, * patterns) :
        for pat in patterns :
            for p in pat.split (";") :
                self.wtk_object.add_pattern (p.strip ())
    # end def add_pattern

# end class File_Filter

if __name__ != "__main__" :
    GTK._Export ("File_Filter")
### __END__ TGL.TKT.GTK.File_Filter
