# -*- coding: iso-8859-15 -*-
# Copyright (C) 2006-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.multimap
#
# Purpose
#    Provide multimap (a dictionary of lists or dicts)
#
# Revision Dates
#    13-Mar-2006 (CT) Creation
#    14-Nov-2006 (CT) `mm_set` added
#    20-Mar-2013 (CT) Derive from `TFL.defaultdict_cb`, not `._defaultdict_`
#    16-Apr-2013 (CT) Add `mm_dict_mm_dict`
#    ��revision-date�����
#--

from   _TFL import      TFL
import _TFL.defaultdict

class mm_dict (TFL.defaultdict_cb) :
    """`defaultdict` with `dict` as `default_factory`.

       >>> mmd = mm_dict (a = {1 : 2, 2 : 4}, b = {42 : 1})
       >>> sorted (mmd.items ())
       [('a', {1: 2, 2: 4}), ('b', {42: 1})]
       >>> "a" in mmd, "d" in mmd
       (True, False)
       >>> sorted (mmd ["a"]), sorted (mmd ["d"])
       ([1, 2], [])
       >>> "a" in mmd, "d" in mmd
       (True, True)
    """

    default_factory = dict

# end class mm_dict

class mm_list (TFL.defaultdict_cb) :
    """`defaultdict` with `list` as `default_factory`.

       >>> mml = mm_list (a = [1], b = [2], c = [42])
       >>> sorted (mml.items ())
       [('a', [1]), ('b', [2]), ('c', [42])]
       >>> "a" in mml, "d" in mml
       (True, False)
       >>> mml ["a"], mml ["d"]
       ([1], [])
       >>> "a" in mml, "d" in mml
       (True, True)
    """

    default_factory = list

# end class mm_list

class mm_set (TFL.defaultdict_cb) :
    """`defaultdict` with `set` as `default_factory`."""

    default_factory = set

# end class mm_set

class mm_dict_mm_dict (TFL.defaultdict_cb) :
    """`defaultdict` with `mm_dict` as `default_factory`."""

    default_factory = mm_dict

# end class mm_dict_mm_dict

class mm_dict_mm_list (TFL.defaultdict_cb) :
    """`defaultdict` with `mm_list` as `default_factory`."""

    default_factory = mm_list

# end class mm_dict_mm_list

multimap = mm_list

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.multimap
