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
#    Model a XML document (i.e., prolog plus root element)
#
# Revision Dates
#    26-Aug-2004 (CT) Creation
#    17-Sep-2004 (CT) Doctest changed (added `%` to document text)
#    21-Oct-2004 (CT) Use `"` instead of `'` in output
#     5-Sep-2005 (CT) Derive from `XML.Node` instead of `XML.Element`
#     5-Sep-2005 (CT) `root_element` added and `insert` redefined to delegate
#                     to `root_element`
#     5-Sep-2005 (CT) Doctest `svg` added
#     6-Sep-2005 (CT) Doctest adapted to change of `_attr_values`
#    20-Sep-2005 (CT) Doctest with over-long attributes added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                   import TFL
import _TFL._SDG._XML.Comment
import _TFL._SDG._XML.Doctype
import _TFL._SDG._XML.Element
import _TFL._SDG._XML.Node

class Document (TFL.SDG.XML.Node) :
    """Model a XML document (i.e., the root element)

       >>> d = Document ( "Memo", "First line of text"
       ...              , "& a second line of %text"
       ...              , "A third line of %text &entity; including"
       ...              , doctype     = "memo"
       ...              , description = "Just a test"
       ...              )
       >>> print chr (10).join (d.formatted ("xml_format"))
       <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
       <!DOCTYPE memo >
       <!-- Just a test -->
       <Memo>
         First line of text
         &amp; a second line of %text
         A third line of %text &entity; including
       </Memo>
       >>> d = Document ( "Memo", "First line of text"
       ...              , "& a second line of %text"
       ...              , "A third line of %text &entity; including"
       ...              , doctype     = TFL.SDG.XML.Doctype
       ...                                  ("memo", dtd = "memo.dtd")
       ...              , description = "Just a test"
       ...              )
       >>> print chr (10).join (d.formatted ("xml_format"))
       <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
       <!DOCTYPE memo SYSTEM "memo.dtd">
       <!-- Just a test -->
       <Memo>
         First line of text
         &amp; a second line of %text
         A third line of %text &entity; including
       </Memo>
       >>> s = Document ( TFL.SDG.XML.Element
       ...                  ( "svg"
       ...                  , x_attrs     = dict
       ...                      ( viewBox = "10 60 450 260"
       ...                      , xmlns   = "http://www.w3.org/2000/svg"
       ...                      , width   = "100%"
       ...                      , height  = "100%"
       ...                      )
       ...                  )
       ...              , "..."
       ...              , encoding        = "UTF-8"
       ...              , standalone      = "no"
       ...              )
       >>> print chr (10).join (s.formatted ("xml_format"))
       <?xml version="1.0" encoding="UTF-8" standalone="no"?>
       <svg height="100%" viewBox="10 60 450 260" width="100%"
            xmlns="http://www.w3.org/2000/svg"
       >
         ...
       </svg>
       >>> attrs = { "xmlns:fx"      : "http://www.asam.net/xml/fbx"
       ...         , "xmlns:ho"      : "http://www.asam.net/xml"
       ...         , "xmlns:flexray" : "http://www.asam.net/xml/fbx/flexray"
       ...         , "xmlns:xsi"
       ...         : "http://www.w3.org/2001/XMLSchema-instance"
       ...         , "xsi:schemaLocation"
       ...         : "http://www.asam.net/xml/fbx/all/fibex4multiplatform.xsd"
       ...         , "VERSION"       : "1.0.0a"
       ...         }
       >>> d = Document (TFL.SDG.XML.Element ("fx:FIBEX", x_attrs = attrs ))
       >>> print chr (10).join (d.formatted ("xml_format"))
       <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
       <fx:FIBEX VERSION="1.0.0a"
                 xmlns:flexray="http://www.asam.net/xml/fbx/flexray"
                 xmlns:fx="http://www.asam.net/xml/fbx"
                 xmlns:ho="http://www.asam.net/xml"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.asam.net/xml/fbx/all/fibex4multiplatform.xsd"
       >
       </fx:FIBEX>
    """

    front_args           = ("root_element", )
    init_arg_defaults    = dict \
        ( doctype        = None
        , encoding       = "iso-8859-1"
        , root_element   = None
        , standalone     = "yes"
        , xml_version    = 1.0
        )

    xml_format           = """
        <?xml version="%(xml_version)s" encoding="%(encoding)s" standalone="%(standalone)s"?>
        %(::*doctype:)s
        %(::*description:)s
        %(::*root_element:)s
    """

    _autoconvert         = dict \
        ( doctype        = lambda s, k, v : s._convert (v, TFL.SDG.XML.Doctype)
        , root_element   = lambda s, k, v : s._convert (v, TFL.SDG.XML.Element)
        , standalone     = lambda s, k, v
                         : { "yes" : "yes"
                           , True  : "yes"
                           , False : "no"
                           , "no"  : "no"
                           } [v]
        )

    def formatted (self, format_name, * args, ** kw) :
        for r in self.__super.formatted (format_name, * args, ** kw) :
            if isinstance (r, unicode) :
                r = r.encode (self.encoding, "xmlcharrefreplace")
            yield r
    # end def formatted

    def insert (self, child, index = None, delta = 0) :
        self.root_element.insert (child, index, delta)
    # end def insert

# end class Document

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Document
