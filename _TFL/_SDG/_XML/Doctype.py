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

class Doctype (TFL.SDG.XML.Element) :
    """Model the doctype declaration of a XML document

       >>> from _TFL._SDG._XML import Decl
       >>> dt = Doctype ( "Test"
       ...              , Decl.Element  ("Test", "(head, body, tail)")
       ...              , Decl.Element  ("head", "(title, author)")
       ...              , Decl.Element  ("body", "(\#PCDATA)")
       ...              , Decl.Element  ("tail", "(disclaimer)")
       ...              , Decl.Attlist  ( "head"
       ...                              , "Date CDATA \#REQUIRED"
       ...                              , "Version CDATA \#REQUIRED"
       ...                              )
       ...              , Decl.Notation ( "GIF", "SYSTEM '/usr/bin/display'")
       ...              , Decl.Entity   ( "entity"
       ...                              , "'An internal general parsed entity'"
       ...                              )
       ...              , Decl.Parameter( "parameter", "<!ELEMENT SAMPLE ANY>")
       ...              , Decl.Unparsed ( "unparsed"
       ...                              , "SYSTEM '/var/local/fubar.gif'"
       ...                              , "GIF"
       ...                              )
       ...              )
       >>> dt.write_to_xml_stream ()
       <!DOCTYPE Test SYSTEM 'Test.dtd'
           <!ELEMENT Test (head, body, tail) >
           <!ELEMENT head (title, author) >
           <!ELEMENT body (\#PCDATA) >
           <!ELEMENT tail (disclaimer) >
           <!ATTLIST head Date CDATA \#REQUIRED
                      Version CDATA \#REQUIRED >
           <!NOTATION GIF SYSTEM '/usr/bin/display' >
           <!ENTITY entity 'An internal general parsed entity' >
           <!ENTITY % parameter <!ELEMENT SAMPLE ANY> >
           <!ENTITY unparsed SYSTEM '/var/local/fubar.gif' NDATA GIF >
       >
    """

    kind                 = "SYSTEM"

    init_arg_defaults    = dict \
        ( doctype        = None
        , dtd            = None
        )

    elem_type            = "DOCTYPE"

    xml_format           = \
        ( """<!DOCTYPE %(doctype)s %(kind)s '%(dtd)s'"""
            """%(:front=%(NL)s%(" " * (indent_offset + 4))s"""
              """¡rear=%(NL)s%(" " * indent_offset)s"""
              """¡sep=%(" " * (indent_offset + 4))s"""
              """:*body_children"""
              """:)s"""
          """>"""
        )

    def __init__ (self, doctype, * etd, ** kw) :
        assert "elem_type" not in kw
        doctype = Filename (doctype).base
        dtd     = Filename (kw.get ("dtd", ""), doctype, ".dtd").name
        self.__super.__init__ \
            (self.elem_type, doctype = doctype, dtd = dtd, * etd, ** kw)
    # end def __init__

# end class Doctype

"""
from _TFL._SDG._XML.Doctype import *
from _TFL._SDG._XML         import Decl
dt = Doctype ( "Test"
             , Decl.Element  ( "Test", "(head, body, tail)")
             , Decl.Element  ( "head", "(title, author)")
             , Decl.Element  ( "body", "(\#PCDATA)")
             , Decl.Element  ( "tail", "(disclaimer)")
             , Decl.Attlist  ( "head"
                             , "Date CDATA \#REQUIRED"
                             , "Version CDATA \#REQUIRED"
                             )
             , Decl.Notation ( "GIF", "SYSTEM 'display")
             , Decl.Entity   ( "entity", "'An internal general parsed entity'")
             , Decl.Unparsed ( "unpe", "/var/local/fubar.gif", "GIF")
             )
dt.write_to_xml_stream ()
"""

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Doctype
