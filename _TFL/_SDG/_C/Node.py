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
#    TFL.SDG.C.Node
#
# Purpose
#    Model a node of the code in a C file
#
# Revision Dates
#    26-Jul-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._C
import _TFL._SDG.Node

from   predicate         import *

H  = 1
C  = 2
HC = H | C

class _C_Node_ (TFL.SDG.Node) :
    """Model a node of the code in a C file"""

    _real_name           = "Node"

    description_level    = 1
    eol_desc_level       = description_level + 4
    star_level           = 1
    pass_scope           = 1
    _end_with_bol        = 1
    ( Body
    , Decl
    , Head
    , Tail
    , Args
    , Incl
    )                    = range (6)

    init_arg_defaults    = dict \
        ( description    = ""
        , eol_desc       = ""
        , scope          = HC
        )

    _autoconvert         = dict \
        ( description    = lambda s, v : s._convert_c_comment (v, False)
        , eol_desc       = lambda s, v : s._convert_c_comment (v, True)
        )

    _list_of_formats     = TFL.SDG.Node._list_of_formats + \
        ( "h_format"
        , "c_format"
        )

    def _update_scope (self, scope) :
        self.scope = self.scope & scope
    # end def _update_scope

    def _update_scope_child (self, child, scope) :
        if self.pass_scope :
            child._update_scope (self.scope)
    # end def _update_scope_child

    def _insert (self, child, index, children, delta = 0) :
        if child :
            self._update_scope_child (child, self.scope)
            self.__super._insert (child, index, children, delta)
    # end def _insert

    def _convert (self, value, Class, * args, ** kw) :
        if value and isinstance (value, str) :
            value = string.strip (value)
            value = Class (value, * args, ** kw)
        return value
    # end def _convert

    def _force (self, value, Class, * args, ** kw) :
        """Comverts `value' to an instance of `Class'."""
        value = self._convert (value, Class, * args, ** kw)
        if not isinstance (value, Class) :
            value = Class (value, * args, ** kw)
        return value
    # end def _force

    def _convert_c_comment (self, attr_name, eol = 0, new_line_col = 0) :
        attr_val  = getattr (self, attr_name)
        if attr_val  and isinstance (attr_val, str) :
            attr_val = (attr_val, )
        if attr_val and isinstance (attr_val, (tuple, list)) :
            setattr ( self, attr_name
                    , TFL.SDG.C.Comment
                          ( *  attr_val
                          , ** dict
                              ( level        = getattr
                                    ( self, "%s_level" % attr_name
                                    , self.description_level
                                    )
                              , stars        = self.star_level
                              , eol          = eol
                              , new_line_col = new_line_col
                              )
                          )
                    )
    # end def _convert_c_comment

    def _convert_c_stmt (self, value) :
        if value and isinstance (value, str) :
            result = []
            for s in value.split (";") :
                stmt = self._convert (s.strip (), TFL.SDG.C.Statement)
                if stmt :
                    result.append (stmt)
        else :
            if isinstance (value, (list, tuple, NO_List)) :
                result = value
            else :
                result = [value]
        return result
    # end def _convert_c_stmt

# end class _C_Node_

Node = _C_Node_

if __name__ != "__main__" :
    TFL.SDG.C._Export ("Node", "H", "C", "HC")
### __END__ TFL.SDG.C.Node
