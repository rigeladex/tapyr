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
