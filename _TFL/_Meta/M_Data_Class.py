# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.M_Data_Class
#
# Purpose
#    Meta class supporting definition of classes holding data
#
# Revision Dates
#    25-Jan-2005 (CT) Creation
#    ««revision-date»»···
#--

"""
M_Data_Class supports the definition of classes holding primarily or
exclusively data in the form of class attributes with full support for
inheritance.

>>> class M_Record (M_Data_Class) :
...     class _allowed (type) :
...         foo = None
...         bar = 42
...         baz = 137
...
>>> R1 = M_Record ("R1", (), dict (foo = 1))
>>> print R1, R1.foo, R1.bar, R1.baz
<Record R1> 1 42 137
>>> R2 = M_Record ("R2", (R1, ), dict (bar = 2))
>>> print R2, R2.foo, R2.bar, R2.baz
<Record R2> 1 2 137
>>> R3 = M_Record ("R3", (R1, ), dict (baz = 3))
>>> print R3, R3.foo, R3.bar, R3.baz
<Record R3> 1 42 3
>>> R4 = M_Record ("R4", (R2, R3), dict ())
>>> print R4, R4.foo, R4.bar, R4.baz
<Record R4> 1 2 3
>>> R5 = M_Record ("R5", (R1, ),   dict (bauz = 5))
Traceback (most recent call last):
  ...
TypeError: <Record R5> doesn't allow attribute bauz=5


from _TFL._Meta.M_Data_Class import *
class M_Record (M_Data_Class) :
    class _allowed (type) :
        foo = None
        bar = 42
        baz = 137

R1 = M_Record ("R1", (),       dict (foo = 1))
R2 = M_Record ("R2", (R1, ),   dict (bar = 2))
R3 = M_Record ("R3", (R1, ),   dict (baz = 3))
R4 = M_Record ("R4", (R2, R3), dict ())
"""

from   _TFL             import TFL
import _TFL._Meta.M_Class

class M_Data_Class (TFL.Meta._M_Type_) :
    """Meta class supporting definition of classes holding data"""

    class _allowed (type) :
        pass
    # end class _allowed

    def __new__ (meta, name, bases, dict) :
        if not bases :
            bases = (meta._allowed, )
        result = super (M_Data_Class, meta).__new__ (meta, name, bases, dict)
        return result
    # end def __new__

    def __init__ (cls, name, bases, dict) :
        _allowed = cls._allowed.__dict__
        for k, v in dict.iteritems () :
            if k not in _allowed :
                raise TypeError, \
                    "%s doesn't allow attribute %s=%r" % (cls, k, v)
        super (M_Data_Class, cls).__init__ (name, bases, dict)
    # end def __init__

    def __repr__ (cls) :
        return "<%s %s>" % (cls.__class__.__name__ [2:], cls.__name__)
    # end def __repr__

# end class M_Data_Class

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.M_Data_Class
