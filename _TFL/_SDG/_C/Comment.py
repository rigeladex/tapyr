# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.SDG.C.Comment
#
# Purpose
#    Model comments in the code in a C file
#
# Revision Dates
#    26-Jul-2004 (CT) Creation
#    27-Jul-2004 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C.Node

"""
from _TFL._SDG._C.Comment import *
c = Comment ("abc", "def", "xyz")
print "\n".join (c.formatted ("h_format"))
print "\n".join (c.as_tree (base_indent = "  "))

"""

class Comment (TFL.SDG.Leaf, TFL.SDG.C.Node) :
    """Comment in a C file"""

    init_arg_defaults    = dict \
        ( level          = 1
        , stars          = 1
        , eol            = 0
        , new_line_col   = 0
        , tail_column    = 79
        )

    out_level            = 1
    eol_comment_head     = 40
    eol_comment_tail     = 79
    electric_break       = 1

    if 0 :
        ### just as demonstration how to use a different but still correct
        ### layout
        h_format = c_format  = """
            /%("*" * stars)s %(:sep=%("*" * stars)s* :.description:)s
            %("*" * stars)s/
        """

    h_format = c_format  = """
        %(:head=/%("*" * stars)s ¡tail= %("*" * stars)s/:.description:)s
    """

    def __init__ (self, * description, ** kw) :
        if description :
            self.__super.__init__ (description = description, ** kw)
        else :
            self.__super.__init__ (** kw)
    # end def __init__

    def _convert_c_comment (self, name, value, ** kw) :
        return value ### avoid endless recursion
    # end def _convert_c_comment

# end class Comment

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Comment
