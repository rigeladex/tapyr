# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.update_combined
#
# Purpose
#    Update a dictionary/list/set with elements of another
#    dictionary/list/set, combining existing keys or values
#
# Revision Dates
#    21-Aug-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _TFL                       import TFL

from   _TFL._Meta.Single_Dispatch import Single_Dispatch, Single_Dispatch_2nd
from   _TFL.Decorator             import Attributed
from   _TFL.pyk                   import pyk

import _TFL._Meta.Object
import _TFL.Undef

_undef = TFL.Undef ("value")

class Dont_Combine (object) :
    """Mixin indicating that the value should replace an existing value,
       instead of combining with it.
    """
# end class Dont_Combine

class dict_dont_combine (Dont_Combine, dict) :
    """Dictionary that doesn't combine, but replaces, under `update_combined`"""
# end class dict_dont_combine

class list_dont_combine (Dont_Combine, list) :
    """List that doesn't combine, but replaces, under `update_combined`"""
# end class list_dont_combine

class set_dont_combine (Dont_Combine, set) :
    """Set that doesn't combine, but replaces, under `update_combined`"""
# end class set_dont_combine

class tuple_dont_combine (Dont_Combine, tuple) :
    """Tuple that doesn't combine, but replaces, under `update_combined`"""
# end class tuple_dont_combine

class filtered_list (TFL.Meta.BaM (list, metaclass = TFL.Meta.M_Class)) :
    """List that filters elements from ``lhs`` when `update_combined` as
       ``rhs``.
    """

    def __init__ (self, * args, ** kw) :
        self.Filter = kw.pop  ("filter")
        assert not kw, kw
        self.__super.__init__ (args)
    # end def __init__

# end class filtered_list

@Single_Dispatch
@Attributed \
    ( Dict_DC  = dict_dont_combine
    , List_DC  = list_dont_combine
    , Set_DC   = set_dont_combine
    , Tuple_DC = tuple_dont_combine
    )
def update_combined (lhs, rhs) :
    """Generic function to update ``lhs`` with the elements of ``rhs``,
       combining existing keys.
    """
    raise NotImplementedError \
        ( "`update_combined` isn't implemented for type `%s`; "
          "got arguments (%r, %r)"
        % (type (lhs), lhs, rhs)
        )
# end def update_combined

@Single_Dispatch_2nd
def update_combined_value (lhs, rhs) :
    """Generic functions for update/combining the values ``lhs`` and ``rhs``.

       Values of types like ``dict``, ``list``, ``set`` combine; values
       derived from ``Dont_Combine`` and of types like ``int``, ``float``,
       ``str`` are replaced by ``rhs``.
    """
    return rhs
# end def update_combined_value

@update_combined.add_type (dict)
def update_combined__dict (lhs, rhs) :
    """Update/combine the dictionary ``lhs`` with the key/value pairs from
       ``rhs``, combining the values of existing keys, if possible.
    """
    if isinstance (rhs, Dont_Combine) :
        result = rhs
    else :
        result = lhs.__class__ (lhs)
        skip   = TFL.is_undefined
        for k, r in pyk.iteritems (rhs) :
            if not skip (r) :
                l = lhs.get (k, _undef)
                result [k] = r if l is _undef else update_combined_value (l, r)
    return result
# end def update_combined__dict

@update_combined.add_type (list, set, tuple)
def update_combined__l_s_t (lhs, rhs) :
    """Update/combine the list/set/tuple ``lhs`` with the elements of ``rhs``."""
    if isinstance (rhs, Dont_Combine) :
        result = rhs
    else :
        result = update_combined_value (lhs, rhs)
    return result
# end def update_combined__l_s_t

@update_combined_value.add_type (dict)
def update_combined_value__dict (lhs, rhs) :
    return update_combined__dict (lhs, rhs)
# end def update_combined_value__dict

@update_combined_value.add_type (filtered_list)
def update_combined_value__filtered_list (lhs, rhs) :
    result  = lhs.__class__ (l for l in lhs if rhs.Filter (l))
    result += rhs
    return result
# end def update_combined_value__filtered_list

@update_combined_value.add_type (list, tuple)
def update_combined_value__list (lhs, rhs) :
    result  = lhs.__class__ (lhs)
    result += rhs
    return result
# end def update_combined_value__list

@update_combined_value.add_type (set)
def update_combined_value__set (lhs, rhs) :
    result  = lhs.__class__ (lhs)
    result |= rhs
    return result
# end def update_combined_value__set

@update_combined_value.add_type (Dont_Combine)
def update_combined_value__dont_combine (lhs, rhs) :
    return rhs
# end def update_combined_value__dont_combine

__doc__ = """
Module `update_combined`
==========================

Update a dictionary/list/set with elements of another
dictionary/list/set, combining existing keys or values, instead of
replacing like the standard ``dict`` method ``update()``does .

    >>> from   _TFL.Formatter           import formatted_1

    >>> l1 = dict (foo = 1, bar = { 1 : "a", 2 : "b"}, qux = [2, 3])
    >>> r1 = dict (bar = { 2 : "baz", 3 : "c" }, qux = [5, 7])
    >>> formatted_1 (l1)
    "{'bar' : {1 : 'a', 2 : 'b'}, 'foo' : 1, 'qux' : [2, 3]}"
    >>> formatted_1 (r1)
    "{'bar' : {2 : 'baz', 3 : 'c'}, 'qux' : [5, 7]}"
    >>> formatted_1 (update_combined (l1, r1))
    "{'bar' : {1 : 'a', 2 : 'baz', 3 : 'c'}, 'foo' : 1, 'qux' : [2, 3, 5, 7]}"

    >>> l2 = dict (bar = list_dont_combine ([1, 2, 3]), qux = [1, 2, 3])
    >>> r2 = dict (bar = [4, 5], qux = list_dont_combine ([4, 5]))
    >>> formatted_1 (l2)
    "{'bar' : [1, 2, 3], 'qux' : [1, 2, 3]}"
    >>> formatted_1 (r2)
    "{'bar' : [4, 5], 'qux' : [4, 5]}"
    >>> formatted_1 (update_combined (l2, r2))
    "{'bar' : [1, 2, 3, 4, 5], 'qux' : [4, 5]}"

    >>> l3 = dict (bar = set ([1, 2, 3]), qux = set ([1, 2, 3]))
    >>> r3 = dict (bar = set ([4, 5]), qux = set_dont_combine ([4, 5]))
    >>> formatted_1 (l3)
    "{'bar' : {1, 2, 3}, 'qux' : {1, 2, 3}}"
    >>> formatted_1 (r3)
    "{'bar' : {4, 5}, 'qux' : {4, 5}}"
    >>> formatted_1 (update_combined (l3, r3))
    "{'bar' : {1, 2, 3, 4, 5}, 'qux' : {4, 5}}"

    >>> l4 = list (range (10))
    >>> r4 = filtered_list (20, 30, 40, filter = lambda x : bool (x % 2))
    >>> formatted_1 (l4)
    '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]'
    >>> formatted_1 (r4)
    '[20, 30, 40]'
    >>> formatted_1 (update_combined (l4, r4))
    '[1, 3, 5, 7, 9, 20, 30, 40]'

    >>> r5 = filtered_list (20, 30, 40, filter = lambda x : not (x % 2))
    >>> formatted_1 (l4)
    '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]'
    >>> formatted_1 (r5)
    '[20, 30, 40]'
    >>> formatted_1 (update_combined (l4, r5))
    '[0, 2, 4, 6, 8, 20, 30, 40]'

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

"""

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.update_combined
