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
#    TFL.SDG.XML.Document
#
# Purpose
#    Model a XML document (i.e., the root element)
#
# Revision Dates
#    26-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._SDG._XML.Comment
import _TFL._SDG._XML.Doctype
import _TFL._SDG._XML.Element

class Document (TFL.SDG.XML.Element) :
    """Model a XML document (i.e., the root element)

       >>> d = Document ("Memo", doctype = "memo", description = "Just a test")
       >>> print chr (10).join (d.formatted ("xml_format"))
       <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
       <!DOCTYPE memo SYSTEM "memo.dtd">
       <!-- Just a test -->
       <Memo>
       </Memo>
    """

    Ancestor             = TFL.SDG.XML.Element

    init_arg_defaults    = dict \
        ( doctype        = None
        , encoding       = "iso-8859-1"
        , standalone     = "yes"
        , xml_version    = 1.0
        )

    xml_format           = """
        <?xml version="%(xml_version)s" encoding="%(encoding)s" standalone="%(standalone)s"?>
        %(::*doctype:)s
    """ + Ancestor._xml_format

    _autoconvert         = dict \
        ( doctype        = lambda s, k, v : s._convert (v, TFL.SDG.XML.Doctype)
        , standalone     = lambda s, k, v
                         : { "yes" : "yes"
                           , True  : "yes"
                           , False : "no"
                           , "no"  : "no"
                           } [v]
        )

# end class Document

"""
d = Document ("Memo", doctype = "memo")
print "\n".join (d.formatted ("xml_format"))
"""
if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Document
