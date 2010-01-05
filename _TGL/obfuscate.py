# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
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
#    TGL.obfuscate
#
# Purpose
#    Obfuscate words
#
# Revision Dates
#    16-Nov-2006 (CT) Creation
#    ««revision-date»»···
#--

"""
Inspired by the text
    According to a researcher at Cambridge
    University, it doesn't matter in what
    order the letters in a word are,
    the only important thing is that the
    first and last letter be at the right
    place. The rest can be a total mess
    and you can still read it without
    problem. This is because the human mind
    does not read every letter by itself,
    but the word as a whole.
obfuscated in
  - http://bitworking.org/projects/cascon06/5.html
  - http://bitworking.org/projects/cascon06/11.html


"""

from   _TGL import TGL
import random
import re

_pat = re.compile (r"""(?<!\w)(\w{4,})(?!\w)""")

def obfuscate_word (word) :
    """Obfuscate `word` by randomly rearranging the inner characters (i.e.,
       all characters but the first and the last).
    """
    inner = list  (word [1:-1])
    orig  = inner [:]
    for i in range (5) :
        random.shuffle (inner)
        if inner != orig :
            break
    return "%s%s%s" % (word [0], "".join (inner), word [-1])
# end def obfuscate_word

def obfuscate (text) :
    return _pat.sub (lambda m : obfuscate_word (m.group (1)), text)
# end def obfuscate

if __name__ != "__main__" :
    TGL._Export ("*")
### __END__ TGL.obfuscate
