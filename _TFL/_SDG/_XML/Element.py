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
#    TFL.SDG.XML.Element
#
# Purpose
#    Model an element of a XML document
#
# Revision Dates
#    26-Aug-2004 (CT) Creation
#    20-Sep-2004 (CT) `x_attrs` added
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._SDG._XML
import _TFL._SDG.Node

from   Regexp            import *

class Element (TFL.SDG.Node) :
    """Model an element of a XML document"""

    attr_names           = ()
    base_indent          = "  "
    front_args           = ("elem_type", )
    init_arg_defaults    = dict \
        ( description    = None
        , elem_type      = None
        , x_attrs        = {}
        )

    _xml_format          = """
        %(::*description:)s
        <%(elem_type)s%(:head= ¡rear0= ¡rear=%(NL)s:>@_attr_values:)s>
        >%(::*body_children:)s
        </%(elem_type)s>
    """.strip ()

    xml_format           = _xml_format

    _autoconvert         = dict \
        ( description    = lambda s, k, v : s._convert (v, TFL.SDG.XML.Comment)
        , elem_type      = lambda s, k, v : s._checked_xml_name (v)
        )

    _xml_name_pat        = Regexp ("[A-Za-z_:][-_:.A-Za-z0-9]*")

    _list_of_formats     = TFL.SDG.Node._list_of_formats + \
        ( "xml_format", )

    _special_char_pat    = Regexp \
        ("[<>]|(&(?! %s;))" % _xml_name_pat.pattern, re.X)
    _special_quot_pat    = Regexp ("&(amp|lt|gt|apos|quot);")

    def as_xml (self, base_indent = None) :
        return self.formatted ("xml_format", base_indent = base_indent)
    # end def as_xml

    def write_to_xml_stream (self, stream = None, gauge = None) :
        """Write `self' and all elements in `self.children' to `stream'.
        """
        self._write_to_stream (self.as_xml (), stream, gauge)
    # end def write_to_xml_stream

    def _attr_values (self, * args, ** kw) :
        attr_values = \
            ( [(a, getattr (self, a)) for a in self.attr_names]
            + self.x_attrs.items ()
            )
        for a, v in attr_values :
            if v is not None :
                v = str (v).replace ("'", "&apos;")
                yield """%s = '%s'""" % (a, v)
    # end def _attr_values

    def _checked_xml_name (self, value) :
        if not self._xml_name_pat.match (value) :
            raise ValueError, "`%s` doesn not match %s" % \
                (value, self._xml_name_pat.pattern)
        return value
    # end def _checked_xml_name

    def _insert (self, child, index, children, delta = 0) :
        if child is not None :
            if isinstance (child, (str, unicode)) :
                import _TFL._SDG._XML.Char_Data
                child = TFL.SDG.XML.Char_Data (child)
            self.__super._insert (child, index, children, delta)
    # end def _insert

    def _special_char_replacer (self, match) :
        return { "&"      : "&amp;"
               , "<"      : "&lt;"
               , ">"      : "&gt;"
               , "'"      : "&apos;"
               , '"'      : "&quot;"
               } [match.group (0)]
    # end def _special_char_replacer

    def _special_quot_replacer (self, match) :
        return { "&amp;"  : "&"
               , "&lt;"   : "<"
               , "&gt;"   : ">"
               , "&apos;" : "'"
               , "&quot;" : '"'
               } [match.group (0)]
    # end def _special_quot_replacer

# end class Element

class Leaf (TFL.SDG.Leaf, Element) :
    """Model a leaf element of a XML document"""

# end class Leaf

class Empty (Leaf) :
    """Model an empty element of a XML document"""

    xml_format           = \
        ( """<%(elem_type)s"""
            """%(:head= ¡rear0= ¡rear=%(NL)s:>@_attr_values:)s"""
          """/>"""
        )

# end class Empty

### for t in Cdata Comment Doctype Document Elem_Type ;
###   do python /swing/python/run_doctest.py $t
###   -p /swing/private/tanzer/lib/python/_TFL/_SDG/_XML ; done

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Element
