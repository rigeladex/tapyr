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
#    TFL.CAL._DTW_
#
# Purpose
#    Root for `datetime` wrappers
#
# Revision Dates
#    14-Oct-2004 (CT) Creation
#    ��revision-date�����
#--

from   _TFL                    import TFL
from   _TFL._CAL.Delta         import Delta
import _TFL._Meta.Object
import  datetime
import  time

class _DTW_ (TFL.Meta.Object) :
    """Root for `datetime` wrappers"""

    _Type            = None
    _kind            = None
    _init_arg_names  = ()
    _timetuple_slice = None

    _body            = property \
        ( lambda self        : getattr (self, self._kind)
        , lambda self, value : setattr (self, self._kind, value)
        )

    formatted = strftime = property (lambda s: s._body.strftime)

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (** kw)
        k = self._kind
        if k in kw :
            assert len (args) == 0
            assert len (kw)   == 1
            self._body = kw [k]
        else :
            args += self._timetuple_slice (time.localtime ()) [len (args):]
            attrs = {}
            for i, name in enumerate (self._init_arg_names) :
                if name in kw :
                    attrs [name] = kw [name]
                else :
                    attrs [name] = args [i]
            self._body = self._Type (** attrs)
    # end def __init__

    def replace (self, ** kw) :
        return self.__class__ (** {self._kind : self._body.replace (** kw)})
    # end def replace

    def _delta (self, delta) :
        result = delta
        if isinstance (delta, (int, long, float)) :
            result = Delta (delta)
        if isinstance (delta, _DTW_) :
            result = delta._body
        return result
    # end def _delta

    def __cmp__ (self, rhs) :
        return cmp (self._body, getattr (rhs, self._kind, rhs))
    # end def __cmp__

    def __hash__ (self) :
        return id (self)
    # end def __hash__

    def __str__ (self) :
        return str (self._body)
    # end def __str__

# end class _DTW_

class _Mutable_DTW_ (TFL.Meta.Object) :
    """Root for mutable `datetime` wrappers"""

    def __init__ (self, * args, ** kw) :
        self._wrapped = self.Class (* args, ** kw)
    # end def __init__

    def replace (self, ** kw) :
        self._wrapped = self._wrapped.replace (** kw)
        return self
    # end def replace

    def __add__ (self, rhs) :
        return self.__class__ (** {self.Class._kind : self._wrapped + rhs})
    # end def __add__

    __cmp__ = property (lambda s : s._wrapped.__cmp__)

    def __getattr__ (self, name) :
        return getattr (self._wrapped, name)
    # end def __getattr__

    def __hash__ (self) :
        raise KeyError, "%s is not hashable"
    # end def __hash__

    def __iadd__ (self, rhs) :
        self._wrapped += rhs
        return self
    # end def __iadd__

    def __isub__ (self, rhs) :
        self._wrapped -= rhs
        return self
    # end def __isub__

    def __sub__ (self, rhs) :
        return self.__class__ (** {self.Class._kind : self._wrapped - rhs})
    # end def __sub__

    __str__ = property (lambda s : s._wrapped.__str__)

# end class _Mutable_DTW_

if __name__ != "__main__" :
    TFL.CAL._Export ("_DTW_", "_Mutable_DTW_")
### __END__ TFL.CAL._DTW_
