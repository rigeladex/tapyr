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
#    TGL.TKT.GTK.Toplevel
#
# Purpose
#    A Toplevel window for applications.
#
# Revision Dates
#    20-May-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Window
import _TGL._TKT._GTK.Signal

class Toplevel (GTK.Window) :
    """A toplevel window for applications."""

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        #self.bind_add (GTK.Signal.Destroy, GTK.quit)
    # end def __init__

# end class Toplevel

if __name__ != "__main__" :
    GTK._Export ("Toplevel")
### __END__ Toplevel
