# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.SDG.XML.External_Id
#
# Purpose
#    Model an external ID
#
# Revision Dates
#     5-Sep-2005 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#     6-Aug-2007 (CED) Future import removed again
#    26-Feb-2012 (MG) `__future__` imports added
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals
from   _TFL                   import TFL
import _TFL._SDG._XML.Node

class External_Id (TFL.SDG.XML.Node) :
    """Model an external ID"""

    kind                 = "SYSTEM"

    front_args           = ("uri", )
    init_arg_defaults    = dict \
        ( uri            = None
        ,
        )

    public_id            = None

    xml_format           = \
        ( """%(kind)s"""
          """%(:front0= ¡front=%(NL)s    """
            """¡rear0=¡rear=%(NL)s"""
            """¡head="¡tail="¡sep=    """
            """:@_ext_ids:)s"""
        )

    def _ext_ids (self, ** kw) :
        if self.public_id is not None :
            yield self.public_id
        if self.uri is not None :
            yield self.uri
    # end def _ext_ids

# end class External_Id

class External_Id_Public (External_Id) :
    """Model a public external ID"""

    kind                 = "PUBLIC"

    front_args           = ("public_id", "uri")
    init_arg_defaults    = dict \
        ( public_id      = None
        )

# end class External_Id_Public

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.External_Id
