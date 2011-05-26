# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.SDG.XML.Elem_Type
#
# Purpose
#    Provide a function for creating new element types dynamically
#
# Revision Dates
#    27-Aug-2004 (CT) Creation
#    20-Sep-2004 (CT) Test for `x_attrs` added
#    21-Oct-2004 (CT) Use `"` instead of `'` in output
#     5-Sep-2005 (CT) Doctest fixed (`x_attrs` sorted alphabetically)
#     6-Sep-2005 (CT) Doctest adapted to change of `_attr_values`
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    20-Nov-2007 (MG)  Imports fixed
#    ««revision-date»»···
#--



"""Usage example:

   >>> from _TFL._SDG._XML.Document import *
   >>> d = Document ("Test", "Test for TFL.SDG.XML.Elem_Type creation and use")
   >>> X = Elem_Type ( "X", foo = None, bar = 42, baz = "quuux")
   >>> Y = Elem_Type ( "Y", bases = (TFL.SDG.XML.Empty, )
   ...               , foo = None, bar = 42, baz = "quuux"
   ...               )
   >>> d.add (X ("A foo-carrying X", foo = "wibble"))
   >>> d.add (Y (bar = "wobble"))
   >>> d.add (X ("A bar-less X", bar = None))
   >>> d.add (Y (baz = None, x_attrs = dict (qux = 84, quy = 85)))
   >>> d.write_to_xml_stream ()
   <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
   <Test>
     Test for TFL.SDG.XML.Elem_Type creation and use
     <X bar="42" baz="quuux" foo="wibble">
       A foo-carrying X
     </X>
     <Y bar="wobble" baz="quuux"/>
     <X baz="quuux">
       A bar-less X
     </X>
     <Y bar="42" qux="84" quy="85"/>
   </Test>

"""
from   _TFL                   import TFL
import _TFL._SDG._XML.Element
import _TFL.Caller

from   _TFL.predicate         import *

def Elem_Type (elem_type, bases = None, front_args = (), rest_args = None, ** attributes) :
    """Return a new subclass of XML.Element"""
    if bases is None :
        bases         = (TFL.SDG.XML.Element, )
    attr_names        = []
    front_dict        = dict_from_list (front_args)
    init_arg_defaults = {}
    for k, v in attributes.iteritems () :
        init_arg_defaults [k] = v
        if not (k in front_dict or k == rest_args) :
            attr_names.append (k)
    return TFL.SDG.XML.Element.__class__ \
        ( elem_type, bases
        , dict ( attr_names        = tuple (sorted (attr_names))
               , elem_type         = elem_type
               , front_args        = front_args
               , init_arg_defaults = init_arg_defaults
               , __module__        = TFL.Caller.globals () ["__name__"]
               , rest_args         = rest_args
               )
        )
# end def Elem_Type

"""
from _TFL._SDG._XML.Document import *
from _TFL._SDG._XML.Elem_Type import *
d = Document ("Test", "Test for TFL.SDG.XML.Elem_Type creation and use")
X = Elem_Type ("X", foo = None, bar = 42, baz = "quuux")
d.add (X ("A foo-carrying X", foo = "wibble"))
d.add (X ("A bar-carrying X", bar = "wobble"))
d.add (X ("A bar-less X", bar = None))
d.write_to_xml_stream ()
"""

if __name__ != "__main__" :
    TFL.SDG.XML._Export ("*")
### __END__ TFL.SDG.XML.Elem_Type
