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
#    TFL.SDG.XML.Char_Data
#
# Purpose
#    Model character data of a XML element
#
# Revision Dates
#    27-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._SDG._XML.Element

class Char_Data (TFL.SDG.XML.Leaf) :
    """Model character data of a XML element"""

    init_arg_defaults    = dict \
        ( text           = None
        )

    front_args           = ()
    rest_args            = "text"

    xml_format           = """%(::.text:)s"""

    _autoconvert         = dict \
        ( text           = lambda s, k, v : s._convert_text (v)
        )

    def _convert_text (self, args) :
        result = []
        for a in args :
            if a and isinstance (a, (str, unicode)) :
                a = self._special_char_pat.sub \
                    (self._special_char_replacer, a).split ("\n")
                result.extend (a)
            else :
                result.append (a)
        return result
    # end def _convert_text

# end class Char_Data

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Char_Data
