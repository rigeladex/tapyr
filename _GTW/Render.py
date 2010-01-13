# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.Render
#
# Purpose
#    Functions for rendering templates
#
# Revision Dates
#    23-May-2008 (CT) Creation
#     8-Jul-2008 (CT) `to_response` added
#    25-May-2009 (CT) `add_replacer` added
#    10-Jan-2010 (MG) Moved into `GTW` package
#    11-Jan-2010 (CT) `to_response` removed
#    13-Jan-2010 (MG) `s/template_env/Templeteer/g`
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _GTW                   import GTW

from   _TFL.Regexp            import *

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

def to_string (template, context, encoding = None, env = None) :
    if env is None :
        from _GTW._NAV.Base import Root
        env = Root.top.Templeteer
    result = env.get_template (template).render (context)
    if encoding is not None :
        result = result.encode (encoding, "replace")
    for rep in _replacers :
        result = rep (result)
    return result
# end def to_string

if __name__ != "__main__":
    GTW._Export_Module ()
### __END__ GTW.Render
