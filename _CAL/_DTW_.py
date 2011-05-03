# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2011 Mag. Christian Tanzer. All rights reserved
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
#    CAL._DTW_
#
# Purpose
#    Root for `datetime` wrappers
#
# Revision Dates
#    14-Oct-2004 (CT) Creation
#    17-Oct-2004 (CT) Use `self.Delta` instead of import
#    17-Oct-2004 (CT) `_delta` changed to not look at `_body`
#    23-Oct-2004 (CT) `formatted` changed to use `_default_format`
#    23-Oct-2004 (CT) `_new_object` factored
#    12-Dec-2004 (CT) `__repr__` added
#     9-Aug-2006 (CT) `__hash__` changed to return `hash (self._body)`
#                     instead of `id (self)`
#    30-Nov-2006 (CT) Empty `__getattr__` added to allow cooperative super
#                     calls for `__getattr__` to fail gracefully
#    12-Dec-2006 (CT) `__init__` changed to use `0` as defaults unless
#                     a True `default_to_now` is passed in
#    12-Dec-2006 (CT) `_new_object` changed from `** kw` to `kw`
#     4-Jan-2007 (CT) `__init__` changed to use `1` for date-fields and `0`
#                     for time-fields as defaults
#     4-Jan-2007 (CT) `__init__` changed to use `localtime` if no args or kw
#                     are passed in (and `default_to_now` removed)
#    31-Mar-2008 (CT) `__init__` changed to dereference `_body` if necessary
#     3-May-2011 (CT) `_init_kw` added and used for `__repr__`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _CAL                    import CAL
import _TFL._Meta.Object
import _TFL.Accessor

import datetime
import time

class _DTW_ (TFL.Meta.Object) :
    """Root for `datetime` wrappers"""

    _Type            = None
    _default_format  = None
    _kind            = None
    _init_arg_names  = ()
    _init_arg_map    = {}
    _timetuple_slice = None

    _body            = property \
        ( lambda self        : getattr (self, self._kind)
        , lambda self, value : setattr (self, self._kind, value)
        )

    strftime         = property (TFL.Getter._body.strftime)

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (** kw)
        k = self._kind
        if k in kw :
            assert len (args) == 0
            assert len (kw)   == 1
            body = kw [k]
            self._init_kw = {}
            if isinstance (body, _DTW_) :
                body = body._body
                self._init_kw = body._init_kw
            self._body = body
        else :
            if len (args) + len (kw) == 0 :
                defaults = time.localtime ()
            else :
                defaults = (1, 1, 1, 0, 0, 0, 0, 0, 0)
            args += self._timetuple_slice (defaults) [len (args):]
            attrs = self._init_kw = {}
            for i, name in enumerate (self._init_arg_names) :
                if name in kw :
                    attrs [name] = kw [name]
                else :
                    attrs [name] = args [i]
            self._body = self._new_object (attrs)
    # end def __init__

    def formatted (self, format = None) :
        if format is None :
            format = self._default_format
        return self.strftime (format)
    # end def formatted

    def replace (self, ** kw) :
        return self.__class__ (** {self._kind : self._body.replace (** kw)})
    # end def replace

    def _delta (self, delta) :
        result = delta
        if isinstance (delta, (int, long, float)) :
            result = self.Delta (delta)
        return result
    # end def _delta

    def _init_arg (self, name) :
        if self._init_kw :
            return self._init_kw.get (name)
        else :
            return getattr (self, self._init_arg_map.get (name, name), 0)
    # end def _init_arg

    def _new_object (self, kw) :
        return self._Type (** kw)
    # end def _new_object

    def __cmp__ (self, rhs) :
        return cmp (self._body, getattr (rhs, self._kind, rhs))
    # end def __cmp__

    def __getattr__ (self, name) :
        raise AttributeError, name
    # end def __getattr__

    def __hash__ (self) :
        return hash (self._body)
    # end def __hash__

    def __repr__ (self) :
        return "%s (%s)" % \
            ( self.__class__.__name__
            , ", ".join
                (repr (self._init_arg (a)) for a in self._init_arg_names)
            )
    # end def __repr__

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
    CAL._Export ("_DTW_", "_Mutable_DTW_")
### __END__ CAL._DTW_
