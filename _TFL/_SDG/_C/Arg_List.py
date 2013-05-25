# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.SDG.C.Arg_List
#
# Purpose
#    Model C argument lists
#
# Revision Dates
#    28-Jul-2004 (CT)  Creation
#     3-Aug-2004 (CT)  Don't redefine the value of `Decl`
#    12-Aug-2004 (MG)  `default_cgi` added
#    13-Aug-2004 (CT)  `base_indent2` replaced by `base_indent * 2`
#    23-Feb-2005 (CED) `apidoc_tex_format` defined
#    08-Dec-2005 (MG)  Bugfixes
#    12-Dec-2005 (CT)  `Regexp` import fixed
#    26-Feb-2012 (MG) `__future__` imports added
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL              import TFL
from   _TFL              import pyk

from   _TFL.predicate    import un_nested
from   _TFL.Regexp       import *
import _TFL._SDG._C.Node
import _TFL._SDG._C.Expression
import _TFL._SDG._C.Var

class Arg_List (TFL.SDG.C.Node) :
    """Model C argument lists"""

    children_group_names = (default_cgi, ) = (TFL.SDG.C.Node.Decl, )

    h_format = c_format  =  apidoc_tex_format = \
        """%(:sep=%(base_indent * 2)s, :*decl_children:)s"""

    arg_pat              = Regexp \
        ( r"^"
          r"(?: "
          r"  (?P<void> void)"
          r"| (?P<type> .+) \s+ (?P<name> [_a-z][_a-z0-9]*)"
          r")"
          r"$"
        , re.VERBOSE | re.IGNORECASE
        )

    def __init__ (self, * children, ** kw) :
        children = un_nested              (children)
        children = self._convert_children (children)
        self.__super.__init__ (* children, ** kw)
    # end def __init__

    def _convert_children (self, children) :
        if len (children) == 1 and isinstance (children [0], pyk.string_types) :
            children = [c.strip () for c in children [0].split (",")]
        result = []
        for c in children :
            if isinstance (c, pyk.string_types) :
                if self.arg_pat.match (c) :
                    if self.arg_pat.void :
                        c = TFL.SDG.C.Expression (self.arg_pat.void)
                    else :
                        c = TFL.SDG.C.Var \
                                (self.arg_pat.type, self.arg_pat.name)
                else :
                    raise TFL.SDG.Invalid_Node (self, c)
            c.cgi     = self.Decl
            c.trailer = ""
            result.append (c)
        return result
    # end def _convert_children

# end class Arg_List

if __name__ != "__main__" :
    TFL.SDG.C._Export ("*")
### __END__ TFL.SDG.C.Arg_List
