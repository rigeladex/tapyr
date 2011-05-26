# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    normalized_indent
#
# Purpose
#    Return string with normalized indentation
#
# Revision Dates
#    14-Mar-2005 (CT) Creation
#     6-Jul-2005 (CT) Doctest moved from function `normalized_indent` to
#                     module (and another case added)
#     6-Jul-2005 (CT) `textwrap.dedent` used if available
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



"""
>>> normalized_indent ("Just a single line.")
'Just a single line.'
>>> normalized_indent ("  Just a single line inside white space.  ")
'Just a single line inside white space.'
>>> print _normalized_indent ('''First line.
...     Second line.
...     Third line.
...         Fourth line (indented).
...         Fifth line (ditto).
...     Sixth line.
... ''')
First line.
Second line.
Third line.
    Fourth line (indented).
    Fifth line (ditto).
Sixth line.
>>> print normalized_indent ('''
...     First line.
...     Second line.
...     Third line.
...         Fourth line (indented).
...         Fifth line (ditto).
...     Sixth line.
... ''')
First line.
Second line.
Third line.
    Fourth line (indented).
    Fifth line (ditto).
Sixth line.
>>> print normalized_indent ('''
...         First line.
...     Second line.
...     Third line.
...         Fourth line (indented).
...         Fifth line (ditto).
...     Sixth line.
...
... ''')
First line.
Second line.
Third line.
    Fourth line (indented).
    Fifth line (ditto).
Sixth line.
>>> print normalized_indent ('''
...  First line.
...     Second line.
...     Third line.
...         Fourth line (indented).
...         Fifth line (ditto).
...     Sixth line.
...
... ''')
First line.
Second line.
Third line.
    Fourth line (indented).
    Fifth line (ditto).
Sixth line.
"""

from   _TFL import TFL

def _normalized_indent (text) :
    """Returns `text` with normalized indentation."""
    lines = text.strip ().split ("\n")
    head  = lines [0]
    rest  = lines [1:]
    if rest :
        indent = 0
        for line in rest :
            contents = line.lstrip ()
            if contents :
                indent = len (line) - len (contents)
                break
        if indent :
            lines = [head] + [line [indent:] for line in rest]
    return "\n".join (lines)
# end def _normalized_indent

try :
    from textwrap import dedent as _dedent
except ImportError :
    normalized_indent = _normalized_indent
else :
    def normalized_indent (text) :
        """Returns `text` with normalized indentation."""
        lines  = text.strip ().split ("\n", 1)
        result = lines [0]
        rest   = lines [1:]
        if rest :
            result = "\n".join ((result, _dedent (rest [0])))
        return result
    # end def normalized_indent

if __name__ != "__main__" :
    TFL._Export ("normalized_indent")
### __END__ normalized_indent
