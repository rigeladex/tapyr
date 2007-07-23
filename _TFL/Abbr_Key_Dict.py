# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Abbr_Key_Dict
#
# Purpose
#    Dictionary supporting unique abbreviations of a key to be used as
#    arguments for `__getitem__'
#
# Revision Dates
#    26-Feb-1999 (CT) Creation
#     8-Apr-1999 (CT) `__init__' added
#    15-Dec-1999 (CT) Inherit from `D_Dict' instead of `UserDict'
#    11-Jun-2003 (CT) s/!= None/is not None/
#    19-Apr-2004 (CT) `really_has_key` added
#    28-Sep-2004 (CT) Use `isinstance` instead of type comparison
#    22-Mar-2005 (MG) Remove `D_Dict` dependency
#    24-Mar-2005 (CT) Doctest added
#    24-Mar-2005 (CT) Small changes in MGs changes
#    24-Mar-2005 (CT) Moved into package `TFL`
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


"""
>>> d = Abbr_Key_Dict (a = 1, ab = 2, abc = 3, bertie = 4, bingo = 5)
>>> d ["a"], d ["ab"], d ["abc"]
(1, 2, 3)
>>> d ["be"], d ["ber"], d ["bertie"]
(4, 4, 4)
>>> d ["b"]
Traceback (most recent call last):
  ...
Ambiguous_Key: "b matches more than 1 key: ['bertie', 'bingo']"
>>> d ["berties"]
Traceback (most recent call last):
  ...
KeyError: 'berties'
>>> d.matching_keys ("a")
['a']
>>> d.matching_keys ("b")
['bertie', 'bingo']
>>> d.matching_keys ("be")
['bertie']
>>> "a" in d, d.has_key ("a")
(True, True)
>>> "ab" in d, d.has_key ("ab")
(True, True)
>>> "abc" in d, d.has_key ("abc")
(True, True)
>>> "b" in d, d.has_key ("b")
(False, False)
>>> "be" in d, d.has_key ("be")
(False, True)
>>> "bertie" in d, d.has_key ("bertie")
(True, True)
"""

from   _TFL      import TFL
import _TFL.predicate

class Ambiguous_Key (KeyError) :
    pass
# end class Ambiguous_Key

class Abbr_Key_Dict (dict) :
    """Dictionary supporting unique abbreviations of a key to be used as
       arguments for `__getitem__'.
    """

    def __getitem__ (self, key) :
        matching = self.matching_keys (key)
        if len (matching) == 1 :
            return super (Abbr_Key_Dict, self).__getitem__ (matching [0])
        elif not matching :
            raise KeyError, key
        else :
            raise Ambiguous_Key, \
                  "%s matches more than 1 key: %s" % (key, matching)
    # end def __getitem__

    def matching_keys (self, abbr) :
        """Returns a list of all keys matching `abbr' if any."""
        if abbr in self :
            return [abbr]
        elif isinstance (abbr, str) :
            return TFL.matches (TFL.sorted (self.iterkeys ()), abbr)
        return []
    # end def matching_keys

    def matching_key (self, abbr) :
        """Returns the key matching `abbr' if any."""
        matching = self.matching_keys (abbr)
        if len (matching) == 1 :
            return matching [0]
    # end def matching_key

    def has_key (self, key) :
        return len (self.matching_keys (key)) == 1
    # end def has_key

    def really_has_key (self, key) :
        return key in self
    # end def really_has_key

# end class Abbr_Key_Dict

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Abbr_Key_Dict
