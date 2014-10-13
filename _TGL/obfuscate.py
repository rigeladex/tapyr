# -*- coding: utf-8 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
