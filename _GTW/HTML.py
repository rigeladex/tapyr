# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.HTML
#
# Purpose
#    Provide HTML related functions for GTW
#
# Revision Dates
#    17-Feb-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW               import GTW

from   _TFL.I18N          import _, _T, _Tn
from   _TFL.Regexp        import *

from   random             import randrange

_obfuscation_format_js = """\
<script type="text/javascript">document.write(String.fromCharCode(%s))</script>\
"""

_obfuscation_format_ns = """\
<noscript>\
<p class="nospam">\
<a class="nospam" title="%s %s">%s</a>\
</p>\
</noscript>\
"""

scheme_map = dict \
    ( mailto = _("email address")
    , tel    = _("phone number")
    )

def obfuscated (text) :
    """Return `text` as (slightly) obfuscated Javascript."""
    js_args = ",".join \
        ( "%s%+d" % (s, c - s)
        for (c, s) in ((ord (c), randrange (1, 256)) for c in text)
        )
    return _obfuscation_format_js % (js_args, )
# end def obfuscated

def obfuscator (scheme = "mailto") :
    need = _T ("Need Javascript for displaying")
    desc = _T (scheme_map.get (scheme, scheme))
    def _rep (match) :
        text = match.group (2)
        js   = obfuscated (match.group (0))
        ns   = _obfuscation_format_ns % (need, desc, text)
        return "".join ((js, ns))
    return Re_Replacer \
        ( r"("
            r"<a"
            r"(?:\s+\w+=" r'"[^"]*"' r")*"
            r"\s+href=" r'"' r"mailto:[^>]+>"
          r")"
          r"([^<]*)"
          r"(</a>)"
        , _rep, re.MULTILINE
        )
# end def obfuscator

if __name__ != "__main__" :
    GTW._Export_Module ()
### __END__ GTW.HTML
