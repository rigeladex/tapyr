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
#    TFL.SDG.XML.Cdata
#
# Purpose
#    Model a CDATA section of a XML document
#
# Revision Dates
#    26-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._SDG._XML.Element

class Cdata (TFL.SDG.XML.Leaf) :
    """Model a CDATA section of a XML document

       >>> c = Cdata ('''<?xml version="1.0"?>
       ... <!DOCTYPE memo SYSTEM "memo.dtd">
       ... <Memo>
       ... </Memo>
       ... ''')
       >>> print chr (10).join (c.formatted ("xml_format"))
       <![CDATA[
         <?xml version="1.0"?>
         <!DOCTYPE memo SYSTEM "memo.dtd">
         <Memo>
         </Memo>
       ]]>
    """

    front_args           = ("data", )
    init_arg_defaults    = dict \
        ( data           = None
        )

    elem_type            = "CDATA"

    xml_format           = """
        <![CDATA[
        >%(::.data:)s
        ]]>
    """

    _autoconvert         = dict \
        ( data           = lambda s, k, v : s._convert_data (v)
        )

    def _convert_data (self, v) :
        if v and isinstance (v, str) :
            assert "]]>" not in v
            v = v.split ("\n")
        return v
    # end def _convert_data

# end class Cdata

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Cdata
