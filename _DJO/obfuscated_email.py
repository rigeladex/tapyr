# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

from   _DJO            import DJO
from   _TFL            import TFL
from   _TFL.Regexp     import *

from   random          import randrange

_fmt_o = """\
<script type="text/javascript">document.write(String.fromCharCode(%s))</script>\
"""
_fmt_p = """\
<noscript>\
<p class="nospam">\
<a class="nospam" title="Need Javascript for Email">%s</a>\
</p>\
</noscript>\
"""
_fmt_t = """\
<noscript>\
<p class="nospam" title="%s">Need Javascript for Email</p>\
</noscript>\
"""

def _gen (text) :
    for c in text :
        yield ord (c), randrange (1, 256)
# end def _gen

def _obf (text) :
    return _fmt_o % \
        (",".join ("%s%+d" % (s, c - s) for (c, s) in _gen (text)))
# end def _obf

def _rep_implicit (match) :
    text = match.group (0)
    js   = _obf (text)
    ns   = _fmt_t % text
    return "".join ((js, ns))
# end def _rep_implicit

def _rep_explicit (match) :
    text = match.group (2)
    js   = _obf (match.group (0))
    ns   = _fmt_p % text
    return "".join ((js, ns))
# end def _rep_explicit

obfuscated_email = Multi_Re_Replacer \
    ( Re_Replacer
        ( r"("
            r"<a"
            r"(?:\s+\w+=" r'"[^"]*"' r")*"
            r"\s+href=" r'"' r"(?:mailto|email):[^>]+>"
          r")"
          r"([^<]*)"
          r"(</a>)"
        , _rep_explicit, re.MULTILINE
        )
    , Re_Replacer
        (r"""\b[-.\w]+(@|&#64;)[-.\w]+\.[a-z]{2,4}\b"""
        , _rep_implicit, re.MULTILINE
        )
    )

if __name__ != "__main__" :
    DJO._Export ("obfuscated_email")
### __END__ obfuscated_email
