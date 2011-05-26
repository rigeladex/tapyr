# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
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
#    DJO.obfuscated_email
#
# Purpose
#    Provide a function for obfuscating email addresses
#
# Revision Dates
#    25-May-2009 (CT) Creation
#     3-Aug-2010 (CT) Completely revamped
#    ««revision-date»»···
#--

from   _DJO            import DJO
from   _TFL            import TFL
from   _TFL.Regexp     import *

from   random          import randrange

_obfuscator_format = """\
<a class="nospam" title="%(need)s" rel="%(js_args)s">%(text)s</a>\
"""

def obfuscated (text) :
    """Return `text` as (slightly) obfuscated Javascript array."""
    result = ",".join \
        ( "%s%+d" % (s, c - s)
        for (c, s) in ((ord (c), randrange (1, 256)) for c in text)
        )
    return result
# end def obfuscated

def _rep (match) :
    return _obfuscator_format % dict \
        ( js_args  = obfuscated  (match.group (0))
        , need     = "Need Javascript for displaying Email"
        , text     = match.group (2)
        )

obfuscated_email = Re_Replacer \
        ( r"(?:"
            r"<a"
            r"("
              r"(?:\s+\w+=" r'"[^"]*"' r")*"
              r"\s+href=" r'"' r"(?:mailto|email):[^>]+>"
            r")"
          r")"
          r"([^<]*)"
          r"(</a>)"
        , _rep, re.MULTILINE
        )

if __name__ != "__main__" :
    DJO._Export ("obfuscated_email")
### __END__ obfuscated_email
