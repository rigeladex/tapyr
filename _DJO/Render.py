# -*- coding: utf-8 -*-
# Copyright (C) 2008-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    25-May-2009 (CT) `add_replacer` added
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

_replacers = [remove_blank_lines]

def add_replacer (* replacers) :
    _replacers.extend (replacers)
# end def add_replacer

def to_response (template, context, encoding = None) :
    return HttpResponse (to_string (template, context, encoding))
# end def to_response

def to_string (template, context, encoding = None) :
    result = render_to_string (template, context).strip ()
    if encoding is not None :
        result = result.encode (encoding, "replace")
    for rep in _replacers :
        result = rep (result)
    return result
# end def to_string

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ DJO.Render
