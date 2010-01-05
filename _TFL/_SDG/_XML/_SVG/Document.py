# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.SDG.XML.SVG.Document
#
# Purpose
#    Model a SVG document
#
# Revision Dates
#     5-Sep-2005 (CT)  Creation
#     6-Sep-2005 (CT)  Creation continued
#     4-Sep-2006 (MZO) `Text` added
#    29-Aug-2008 (CT)  Doctest corrected
#    ««revision-date»»···
#--

"""
>>> svg = Document (Root (width="12cm", height="4cm", viewBox="0 0 1200 400"))
>>> svg.add (Rect
...   (x="1", y="1", width="1198", height="398", fill="none", stroke="blue"))
>>> svg.add (Rect
...   (x="100", y="100", width="400", height="200", rx="50", fill="green"))
>>> svg.add (Group
...   (Rect (x="0", y="0", width="400", height="200", rx="50", fill="none", stroke="purple"), transform="translate(700 210) rotate(-30)"))
>>> svg.add (Circle (cx="600", cy="200", r="100", fill="red", stroke="blue"))
>>> svg.add (Ellipse (rx="250", ry="100", fill="red"))
>>> svg.add (Ellipse
...   (transform="translate(900 200) rotate(-30)", rx="250", ry="100",
...   fill="none", stroke="blue"))
>>> svg.add (Line (x1="100", y1="300", x2="300", y2="100"))
>>> svg.add (Polyline
...   (fill="none", stroke="blue",
...   points="50,375 150,375 150,325 250,325 250,375 350,375 350,250 "
...   "450,250 450,375 550,375 550,175 650,175 650,375 750,375 750,100 "
...   "850,100 850,375 950,375 950,25 1050,25 1050,375 1150,375"))
>>> svg.add (Polygon
...   (fill="red", stroke="blue",
...   points="350,75  379,161 469,161 397,215 423,301 350,250 277,301 "
...   "303,215 231,161 321,161"))
>>> svg.write_to_xml_stream ()
<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
<!DOCTYPE svg PUBLIC
    "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg height="4cm" version="1.1" viewBox="0 0 1200 400" width="12cm"
     xmlns="http://www.w3.org/2000/svg"
>
  <rect fill="none" height="398" stroke="blue" width="1198" x="1" y="1"/>
  <rect fill="green" height="200" rx="50" width="400" x="100" y="100"/>
  <g id="1" transform="translate(700 210) rotate(-30)">
    <rect fill="none" height="200" rx="50" stroke="purple" width="400" x="0"
          y="0"
    />
  </g>
  <circle cx="600" cy="200" fill="red" r="100" stroke="blue"/>
  <ellipse fill="red" rx="250" ry="100"/>
  <ellipse fill="none" rx="250" ry="100" stroke="blue"
           transform="translate(900 200) rotate(-30)"
  />
  <line x1="100" x2="300" y1="300" y2="100"/>
  <polyline fill="none"
            points="50,375 150,375 150,325 250,325 250,375 350,375 350,250 450,250 450,375 550,375 550,175 650,175 650,375 750,375 750,100 850,100 850,375 950,375 950,25 1050,25 1050,375 1150,375"
            stroke="blue"
  />
  <polygon fill="red"
           points="350,75  379,161 469,161 397,215 423,301 350,250 277,301 303,215 231,161 321,161"
           stroke="blue"
  />
</svg>
"""

from   _TFL                   import TFL
import _TFL._SDG._XML.Document
import _TFL._SDG._XML.Elem_Type
import _TFL._SDG._XML._SVG

class _SVG_Document_ (TFL.SDG.XML.Document) :
    """Model a SVG document.

       >>> svg = Document (Root ())
       >>> svg.write_to_xml_stream ()
       <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
       <!DOCTYPE svg PUBLIC
           "-//W3C//DTD SVG 1.1//EN"
           "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
       <svg version="1.1" xmlns="http://www.w3.org/2000/svg">
       </svg>
       >>> svg = Document (
       ...     Root (viewBox="10 60 450 260", width="100%", height="100%"))
       >>> svg.write_to_xml_stream (output_width = 65)
       <?xml version="1.0" encoding="iso-8859-1" standalone="yes"?>
       <!DOCTYPE svg PUBLIC
           "-//W3C//DTD SVG 1.1//EN"
           "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
       <svg height="100%" version="1.1" viewBox="10 60 450 260"
            width="100%" xmlns="http://www.w3.org/2000/svg"
       >
       </svg>
    """

    _real_name           = "Document"

    init_arg_defaults    = dict \
        ( doctype        = TFL.SDG.XML.Doctype
            ( "svg"
            , dtd = TFL.SDG.XML.External_Id_Public
                ( "-//W3C//DTD SVG 1.1//EN"
                , "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"
                )
            )
        )

    _autoconvert         = dict \
        ( root_element   = lambda s, k, v
                         : s._convert (v, TFL.SDG.XML.SVG.Root)
        ,
        )

Document = _SVG_Document_ # end class _SVG_Document_

_shape_attr          = dict \
    ( fill           = None
    , stroke         = None
    , transform      = None
    , x              = None
    , y              = None
    )

Circle               = TFL.SDG.XML.Elem_Type \
    ( "circle"
    , (TFL.SDG.XML.Empty, )
    , cx             = None
    , cy             = None
    , r              = None
    , ** _shape_attr
    )

Ellipse              = TFL.SDG.XML.Elem_Type \
    ( "ellipse"
    , (TFL.SDG.XML.Empty, )
    , cx             = None
    , cy             = None
    , rx             = None
    , ry             = None
    , ** _shape_attr
    )

Group                = TFL.SDG.XML.Elem_Type \
    ( "g"
    , id             = None
    , ** _shape_attr
    )

Line                 = TFL.SDG.XML.Elem_Type \
    ( "line"
    , (TFL.SDG.XML.Empty, )
    , x1             = None
    , x2             = None
    , y1             = None
    , y2             = None
    , ** _shape_attr
    )

Path                 = TFL.SDG.XML.Elem_Type \
    ( "path"
    , d              = None
    , pathLength     = None
    , ** _shape_attr
    )

Polygon              = TFL.SDG.XML.Elem_Type \
    ( "polygon"
    , (TFL.SDG.XML.Empty, )
    , points         = None
    , ** _shape_attr
    )

Polyline             = TFL.SDG.XML.Elem_Type \
    ( "polyline"
    , (TFL.SDG.XML.Empty, )
    , points         = None
    , ** _shape_attr
    )

Rect                 = TFL.SDG.XML.Elem_Type \
    ( "rect"
    , (TFL.SDG.XML.Empty, )
    , height         = None
    , rx             = None
    , ry             = None
    , width          = None
    , ** _shape_attr
    )

Root                 = TFL.SDG.XML.Elem_Type \
    ( "svg"
    , height         = None
    , version        = "1.1"
    , viewBox        = None
    , width          = None
    , xmlns          = "http://www.w3.org/2000/svg"
    , x              = None
    , y              = None
    )

Text                 = TFL.SDG.XML.Elem_Type \
    ( "text"
    , ** _shape_attr
    )

"""
from _TFL._SDG._XML._SVG.Document import *
svg = Document (Root (width="12cm", height="4cm", viewBox="0 0 1200 400"))
svg.add (Rect (x="1", y="1", width="1198", height="398", fill="none", stroke="blue"))
svg.add (Rect (x="100", y="100", width="400", height="200", rx="50", fill="green"))
svg.add (Group (Rect (x="0", y="0", width="400", height="200", rx="50", fill="none", stroke="purple"), transform="translate(700 210) rotate(-30)"))
svg.add (Circle (cx="600", cy="200", r="100", fill="red", stroke="blue"))
svg.add (Ellipse (rx="250", ry="100", fill="red"))
svg.add (Ellipse (transform="translate(900 200) rotate(-30)", rx="250", ry="100", fill="none", stroke="blue"))
svg.add (Line (x1="100", y1="300", x2="300", y2="100"))
svg.add (Polyline (fill="none", stroke="blue", points="50,375 150,375 150,325 250,325 250,375 350,375 350,250 450,250 450,375 550,375 550,175 650,175 650,375 750,375 750,100 850,100 850,375 950,375 950,25 1050,25 1050,375 1150,375"))
svg.add (Polygon (fill="red", stroke="blue", points="350,75  379,161 469,161 397,215 423,301 350,250 277,301 303,215 231,161 321,161"))
svg.write_to_xml_stream ()

"""

if __name__ != "__main__" :
    TFL.SDG.XML.SVG._Export ("*")
### __END__ TFL.SDG.XML.SVG.Document
