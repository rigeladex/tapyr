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
#    TFL.SDG.XML.Doctype
#
# Purpose
#    Model the doctype declaration of a XML document
#
# Revision Dates
#    26-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._SDG._XML.Element

from   Filename               import Filename

class Doctype (TFL.SDG.XML.Leaf) :
    """Model the doctype declaration of a XML document"""

    init_arg_defaults    = dict \
        ( doctype        = None
        , dtd            = None
        , kind           = "SYSTEM"
        )

    elem_type            = "DOCTYPE"

    xml_format           = """<!DOCTYPE %(doctype)s %(kind)s "%(dtd)s">"""

    def __init__ (self, doctype, dtd = None, ** kw) :
        assert "elem_type" not in kw
        doctype = Filename (doctype).base
        dtd     = Filename (dtd or "", doctype, ".dtd").name
        self.__super.__init__ \
            (self.elem_type, doctype = doctype, dtd = dtd, ** kw)
    # end def __init__

# end class Doctype

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Doctype
