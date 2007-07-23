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
#    TFL.SDG.XML.Comment
#
# Purpose
#    Model a comment of a XML document
#
# Revision Dates
#    26-Aug-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL                   import TFL
import _TFL._SDG._XML.Element

class Comment (TFL.SDG.XML.Leaf) :
    """Model a comment of a XML document

       >>> c = Comment ("Just a test of a XML comment -- with illicit token")
       >>> print chr (10).join (c.formatted ("xml_format"))
       <!-- Just a test of a XML comment ··· with illicit token -->
       >>> c = Comment ('''A two line
       ... comment for a change''')
       >>> print chr (10).join (c.formatted ("xml_format"))
       <!-- A two line
            comment for a change
       -->
    """

    front_args           = ("text", )
    init_arg_defaults    = dict \
        ( text           = None
        )

    elem_type            = "!--"

    xml_format           = """
        <!-- %(:rear0= ¡rear=%(NL)s:>.text:)s-->
    """

    _autoconvert         = dict \
        ( text           = lambda s, k, v : s._convert_text (v)
        )

    def _convert_text (self, v) :
        if v and isinstance (v, (str, unicode)) :
            v = v.replace ("--", "···").split ("\n")
        return v
    # end def _convert_text

# end class Comment

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Comment
