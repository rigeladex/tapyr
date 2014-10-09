# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
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
#    TFL.portable_repr
#
# Purpose
#    Portable replacement for `repr` giving identical results in Python 2 & 3
#
# Revision Dates
#     9-Oct-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__                 import division, print_function
from   __future__                 import absolute_import

from   _TFL                       import TFL

from   _TFL._Meta.Single_Dispatch import Single_Dispatch
from   _TFL.pyk                   import pyk

import sys

__doc__ = r"""
``portable_repr`` returns a portable canonical string
representation of `obj`.

For most object types, ``eval (portable_repr (object)) == object``.

Examples::

    >>> print (portable_repr ([1,2,3, "a", u"b", "c"]))
    [1, 2, 3, 'a', 'b', 'c']

    >>> print (portable_repr ({ 1: u"a", 2: "b", "c" : 23, u"d" : 42 }))
    {'c', 23, 'd', 42, 1, 'a', 2, 'b'}

    >>> print (portable_repr (1 << 65))
    36893488147419103232

    >>> import math
    >>> print (portable_repr (math.pi))
    3.14159265359

    >>> class C (object) :
    ...     class D (object) :
    ...         pass

    >>> print (portable_repr (C))
    <class 'portable_repr.C'>

    >>> print (portable_repr (C.D))
    <class 'portable_repr.D'>

    >>> print (portable_repr (dict))
    <class 'builtins.dict'>

    >>> print (portable_repr (type (u"")))
    <class 'builtins.<text-string>'>

    >>> print (portable_repr (type (b"")))
    <class 'builtins.<byte-string>'>

    >>> print (portable_repr (type (1 << 65)))
    <class 'builtins.int'>

"""

builtin_repr = repr

@Single_Dispatch
def portable_repr (obj) :
    """Return a portable canonical string representation of `obj`.

       For many object types, eval (portable_repr (object)) == object.
    """
    return builtin_repr (obj)
# end def portable_repr

@portable_repr.add_type (dict)
def portable_repr_dict (obj) :
    return "".join \
        ( ( "{"
          , ( ", ".join
                ( sorted
                    ( ", ".join ([portable_repr (k), portable_repr (v)])
                    for k, v in pyk.iteritems (obj)
                    )
                )
            )
          , "}"
          )
        )
# end def portable_repr_dict

@portable_repr.add_type (float)
def portable_repr_float (obj) :
    return "%.12g" % obj
# end def portable_repr_float

@portable_repr.add_type (list, tuple)
def portable_repr_list_tuple (obj) :
    empty = builtin_repr (obj.__class__ ())
    return "".join \
        ( ( empty [0]
          , (", ".join (portable_repr (x) for x in obj))
          , empty [-1]
          )
        )
# end def portable_repr_list_tuple

@portable_repr.add_type (type)
def portable_repr_type (obj) :
    m_name = obj.__module__
    if m_name == "__builtin__" :
        m_name = "builtins"
    t_name = _type_name_map.get (obj.__name__, obj.__name__)
    return "<class %s>" % portable_repr (".".join ((m_name, t_name)))
# end def portable_repr_type

if sys.version_info < (3,) :
    _type_name_map = dict \
        ( bytes    = "<byte-string>"
        , long     = "int"
        , str      = "<byte-string>"
        , unicode  = "<text-string>"
        )

    @portable_repr.add_type (long)
    def portable_repr_long (obj) :
        return builtin_repr (obj).rstrip ("L")
    # end def portable_repr_long

    @portable_repr.add_type (unicode)
    def portable_repr_unicode (obj) :
        return builtin_repr (obj) [1:]
    # end def portable_repr_unicode

else : ### Python version >= 3
    _type_name_map = dict \
        ( bytes    = "<byte-string>"
        , str      = "<text-string>"
        )

__all__ = ("portable_repr", )

if __name__ != "__main__" :
    TFL._Export (* __all__)
### __END__ TFL.portable_repr
