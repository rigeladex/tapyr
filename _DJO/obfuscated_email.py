# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    22-Feb-2012 (CT) Change `_obfuscator_format` so it's valid html5
#    ««revision-date»»···
#--

from   _DJO            import DJO
from   _TFL            import TFL
from   _TFL.Regexp     import *

from   random          import randrange

_obfuscator_format = """\
<a class="nospam" title="%(need)s">%(text)s</a>\
<b class="nospam" title="%(js_args)s"></b>\
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
