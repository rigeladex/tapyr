# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CAL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    CAL.date_time_localizer
#
# Purpose
#    Convert date-times given with tzoffset into local time without tzoffset
#
# Revision Dates
#    30-Mar-2012 (CT) Creation
#    18-Apr-2012 (CT) Use `I18N.decode` and `pyk.fprint`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, unicode_literals

from   _TFL             import TFL
from   _CAL             import CAL

from   _TFL.Regexp      import Regexp, Multi_Re_Replacer, Re_Replacer, re
from   _TFL.pyk         import pyk

import _CAL.Date_Time
import _TFL.CAO
import _TFL.I18N

date_time_localizer_pattern = Regexp \
    ( ( r"(?P<head> ^|[[(\s])"
        r"(?P<year>  \d{4,4})"
        r"([-/]?)"
        r"(?P<month> \d{2,2})"
        r"\3"
        r"(?P<day>   \d{2,2})"
        r"[T ]"
      )
    + CAL.Date_Time.time_pattern.pattern
    + r"(?P<tail> $|[])\s])"
    , flags = re.VERBOSE | re.IGNORECASE
    )
_cleaned = Multi_Re_Replacer \
    ( Re_Replacer (r"^[[(\s]", "")
    , Re_Replacer (r"[])\s]$", "")
    )

def date_time_localizer \
        (s, format = "%Y-%m-%d %H:%M", pattern = None, count = 0) :
    """Convert date-times in `s` into local time without tzoffset.

    >>> date_time_localizer ("09d82ac 2012-03-29 21:06:26 +0200 martin@mangari.org")
    u'09d82ac 2012-03-29 21:06 martin@mangari.org'
    >>> date_time_localizer ("f6baffa 2012-03-29 10:06:46 -0400 martin@mangari.org")
    u'f6baffa 2012-03-29 16:06 martin@mangari.org'
    >>> date_time_localizer ("f99a29d 2005-03-22 09:34:40 +0000 tanzer@swing.co.at")
    u'f99a29d 2005-03-22 10:34 tanzer@swing.co.at'

    """
    if pattern is None :
        pattern = date_time_localizer_pattern
    def repl (match) :
        value  = _cleaned (match.group (0))
        local  = CAL.Date_Time.from_string (value).as_local ()
        result = "%s%s%s" % \
            ( match.group     ("head")
            , local.formatted (format)
            , match.group     ("tail")
            )
        return result
    return pattern.sub (repl, s, count)
# end def date_time_localizer

def _main (cmd) :
    import fileinput
    lines = fileinput.input (cmd.argv)
    if cmd.output :
        sys.stdout = open (cmd.output, "a")
    for l in lines :
        if isinstance (l, str) :
            l = TFL.I18N.decode (l)
        ll = date_time_localizer (l, cmd.format)
        try :
            pyk.fprint (ll, end = "")
        except IOError :
            import sys
            sys.exit (0)
    pyk.fprint ()
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "file:P?Files to convert times for (default: stdin)"
        ,
        )
    , opts          =
        ( "-format:S=%Y-%m-%d %H:%M"
            "?Output format for converted date-time values"
        , "-output:S?Name of file to which to write output (default: stdout)"
        )
    , min_args      = 0
    , description   =
        "Convert date-times in input into local time without tzoffset"
    )

if __name__ != "__main__" :
    CAL._Export ("*")
if __name__ == "__main__" :
    _Command ()
### __END__ CAL.date_time_localizer
