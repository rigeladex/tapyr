# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    Ascii
#
# Purpose
#    Functions for unicode/ASCII handling
#
# Revision Dates
#     6-Sep-2004 (CT) Creation
#    13-May-2005 (CT) Call to `strip` added to `sanitized_filename`
#    ««revision-date»»···
#--

from   _TFL        import TFL
from   _TFL.Regexp import Regexp, re

_diacrit_map    = \
    { u"À"      : u"A"
    , u"Á"      : u"A"
    , u"Â"      : u"A"
    , u"Ã"      : u"A"
    , u"Ä"      : u"Ae"
    , u"Å"      : u"A"
    , u"Æ"      : u"Ae"
    , u"Ç"      : u"C"
    , u"È"      : u"E"
    , u"É"      : u"E"
    , u"Ê"      : u"E"
    , u"Ë"      : u"E"
    , u"Ì"      : u"I"
    , u"Í"      : u"I"
    , u"Î"      : u"I"
    , u"Ï"      : u"I"
    , u"Ð"      : u"D"
    , u"Ñ"      : u"N"
    , u"Ò"      : u"O"
    , u"Ó"      : u"O"
    , u"Ô"      : u"O"
    , u"Õ"      : u"O"
    , u"Ö"      : u"O"
    , u"Ø"      : u"O"
    , u"Ù"      : u"U"
    , u"Ú"      : u"U"
    , u"Û"      : u"U"
    , u"Ü"      : u"U"
    , u"Ý"      : u"Y"
    , u"ß"      : u"ss"
    , u"à"      : u"a"
    , u"á"      : u"a"
    , u"â"      : u"a"
    , u"ã"      : u"a"
    , u"ä"      : u"ae"
    , u"å"      : u"a"
    , u"æ"      : u"ae"
    , u"ç"      : u"c"
    , u"è"      : u"e"
    , u"é"      : u"e"
    , u"ê"      : u"e"
    , u"ë"      : u"e"
    , u"ì"      : u"i"
    , u"í"      : u"i"
    , u"î"      : u"i"
    , u"ï"      : u"i"
    , u"ð"      : u"o"
    , u"ñ"      : u"n"
    , u"ò"      : u"o"
    , u"ó"      : u"o"
    , u"ô"      : u"o"
    , u"õ"      : u"o"
    , u"ö"      : u"oe"
    , u"ø"      : u"o"
    , u"ù"      : u"u"
    , u"ú"      : u"u"
    , u"û"      : u"u"
    , u"ü"      : u"ue"
    , u"ý"      : u"y"
    , u"\u0255" : u"y"
    , u"\u0160" : u" "
    , u"¦"      : u"|"
    , u"¨"      : u'"'
    , u"«"      : u"<<"
    , u"´"      : u"'"
    , u"µ"      : u"u"
    , u"·"      : u"."
    , u"»"      : u">>"
    }

_diacrit_pat    = Regexp \
    (u"|".join  ([re.escape (x) for x in _diacrit_map.iterkeys ()]))

_graph_pat      = Regexp \
    ( "(%s)+"
    % "|".join   ([re.escape (c) for c in ("^!$%&([{}]) ?`'*+#:;<>|" '"')])
    )

_non_print_pat  = Regexp \
    ("|".join   ([re.escape (chr (i)) for i in range (0, 32) + [127]]))

def _diacrit_sub (match) :
    return _diacrit_map.get (match.group (0), "")
# end def _diacrit_sub

def sanitized_unicode (s) :
    """Return sanitized version of unicode string `s` reduced to
       pure ASCII 8-bit string. Caveat: passing in an 8-bit string with
       diacriticals won't work as expected.

       >>> sanitized_unicode (u"üaöbc¡ha!")
       'ueaoebcha!'
    """
    s = _diacrit_pat.sub (_diacrit_sub, s)
    s = s.encode ("us-ascii", "ignore")
    return s
# end def sanitized_unicode

def sanitized_filename (s) :
   """Return `sanitized (s)` with all non-printable and some graphic
      characters removed so that the result is usable as a filename.

       >>> sanitized_filename (
       ...    u"überflüßig komplexer und $gefährlicher* Filename")
       'ueberfluessig_komplexer_und_gefaehrlicher_Filename'
   """
   s = sanitized_unicode  (s.strip ())
   s = _non_print_pat.sub ("",  s)
   s = _graph_pat.sub     ("_", s)
   return s
# end def sanitized_filename

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ Ascii
