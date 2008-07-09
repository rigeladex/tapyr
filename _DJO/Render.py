# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Render
#
# Purpose
#    Functions for rendering templates
#
# Revision Dates
#    23-May-2008 (CT) Creation
#     8-Jul-2008 (CT) `to_response` added
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _DJO                   import DJO

from   _TFL.Regexp            import *

from   django.template.loader import render_to_string
from   django.http            import HttpResponse

remove_blank_lines = Multi_Re_Replacer \
    ( Re_Replacer
        ("[ \t]*\\\\[ \t]*\n[ \t]*([<>])", r"\1",      re.MULTILINE)
    , Re_Replacer
        ("([<>])[ \t]*\\\\[ \t]*\n[ \t]*", r"\1",      re.MULTILINE)
    , Re_Replacer
        ("[ \t]*\\\\[ \t]*\n[ \t]*", " ",              re.MULTILINE)
    , Re_Replacer
        (">[ \t]*\n(?:[ \t]*\n)+([ \t]*)<", r">\n\1<", re.MULTILINE)
    , Re_Replacer
        ("[ \t]*\n(?:[ \t]*\n)*[ \t]*(/?)>", r" \1>",  re.MULTILINE)
    )

def to_response (template, context, encoding = None) :
    return HttpResponse (to_string (template, context, encoding))
# end def to_response

def to_string (template, context, encoding = None) :
    result = render_to_string (template, context)
    if encoding is not None :
        result = result.encode (encoding, "replace")
    result = remove_blank_lines (result.strip ())
    return result
# end def to_string

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ DJO.Render
