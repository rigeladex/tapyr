# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2006 Mag. Christian Tanzer. All rights reserved
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
#     9-Aug-2006 (CT) Use `unicodedata.normalize` (and simplify `_diacrit_map`)
#     9-Mar-2007 (CT) `_diacrit_map` corrected (`Oe` and `Ue` instead `O`/`U`)
#     9-Mar-2007 (CT) Optional `translate_table` added to `sanitized_unicode`
#                     and `sanitized_filename`
#    ««revision-date»»···
#--

from   _TFL        import TFL
from   _TFL.Regexp import Regexp, re
import unicodedata

_diacrit_map    = \
    { u"Ä"      : u"Ae"
    , u"Ö"      : u"Oe"
    , u"Ü"      : u"Ue"
    , u"ß"      : u"ss"
    , u"ä"      : u"ae"
    , u"ö"      : u"oe"
    , u"ü"      : u"ue"
    }

_diacrit_pat    = Regexp \
    (u"|".join  (re.escape (x) for x in _diacrit_map.iterkeys ()))

_graph_pat      = Regexp \
    ( "(%s)+"
    % "|".join   (re.escape (c) for c in ("^!$%&([{}]) ?`'*+#:;<>|" '"'))
    )

_non_print_pat  = Regexp \
    ("|".join   (re.escape (chr (i)) for i in range (0, 32) + [127]))

def _diacrit_sub (match) :
    return _diacrit_map.get (match.group (0), "")
# end def _diacrit_sub

def sanitized_unicode (s, translate_table = None) :
    """Return sanitized version of unicode string `s` reduced to
       pure ASCII 8-bit string. Caveat: passing in an 8-bit string with
       diacriticals doesn't work.

       >>> sanitized_unicode (u"üxäyözßuÜXÄYÖZbc¡ha!")
       'uexaeyoezssuUeXAeYOeZbcha!'
       >>> sanitized_unicode (u"«ÄÖÜ»", {ord (u"«") : u"<", ord ("»") : u">"})
       '<AeOeUe>'
    """
    s = _diacrit_pat.sub (_diacrit_sub, s)
    if translate_table :
        s = s.translate (translate_table)
    return unicodedata.normalize ("NFKD", s).encode ("ascii", "ignore")
# end def sanitized_unicode

def sanitized_filename (s, translate_table = None) :
   """Return `sanitized (s)` with all non-printable and some graphic
      characters removed so that the result is usable as a filename.

       >>> sanitized_filename (
       ...    u"überflüßig komplexer und $gefährlicher* Filename")
       'ueberfluessig_komplexer_und_gefaehrlicher_Filename'
   """
   s = sanitized_unicode  (s.strip (), translate_table)
   s = _non_print_pat.sub ("",  s)
   s = _graph_pat.sub     ("_", s)
   return s
# end def sanitized_filename

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ Ascii
