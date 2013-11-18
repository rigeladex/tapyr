# -*- coding: utf-8 -*-
# Copyright (C) 2000-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.Record
#
# Purpose
#    Class emulating a struct/record (but dynamically)
#
# Revision Dates
#    14-Jun-2000 (CT) Creation
#    11-Sep-2000 (CT) `quote' added to `str'
#    21-Jan-2001 (CT) `__getattr__' uses `try/except' instead of `has_key'
#    16-Apr-2003 (CT) `copy` added
#    21-Jan-2006 (MG)  Moved into `TFL` package
#    20-Mar-2006 (CT)  `__getitem__` added
#    31-May-2006 (WPR) `__iter__` added
#    19-Oct-2007 (PGO) self.kw needs name-mangling, otherwise a stored dict
#                      named `kw` will be silently modified
#     8-Nov-2007 (CT)  Use `_kw` instead of `__kw` (and modernized)
#     8-Nov-2007 (CT)  `assert` statements added to avoid silent errors
#    23-Jan-2008 (CT)  `Record_S` added
#     1-Feb-2008 (MG)  `__nonzero__` added
#    27-Feb-2009 (CT)  `__setitem__` added
#     9-Dec-2009 (CT)  `__delattr__` added
#     9-Dec-2009 (CT) `__repr__` and `_formatted_kw` changed (use `%r`
#                     instead of explicitly quoted `%s`)
#    21-Dec-2009 (CT) `__getstate__` and `__setstate__` added
#    20-Feb-2010 (CT) `__contains__` added
#    20-Jul-2011 (CT) `_properties` added to allow subclasses to define
#                     property setters that actually work
#    ««revision-date»»···
#--

from   _TFL           import TFL
from   _TFL.pyk       import pyk

from   _TFL.predicate import sorted

import _TFL._Meta.Object

class Record (TFL.Meta.Object) :
    """Class emulating a struct/record (but dynamically).

       >>> r = Record (x = "y", kw = dict (foo = 42))
       >>> r.x
       'y'
       >>> r.kw
       {'foo': 42}
    """

    _properties = ()

    def __init__ (self, ** kw) :
        assert "_kw"           not in kw
        assert "copy"          not in kw
        assert "_formatted_kw" not in kw
        assert "_properties"   not in kw
        assert not any (p in kw for p in self._properties)
        self.__dict__ ["_kw"] = kw.copy ()
    # end def __init__

    def copy (self, ** kw) :
        result = self.__class__ (** self._kw)
        result._kw.update (kw)
        return result
    # end def copy

    def _formatted_kw (self) :
        return ", ".join \
            ( (   "%s = %r" % (k, v)
              for (k, v) in sorted (pyk.iteritems (self._kw))
              )
            )
    # end def _formatted_kw

    def __contains__ (self, item) :
        return item in self._kw
    # end def __contains__

    def __delattr__ (self, name) :
        del self._kw [name]
    # end def __delattr__

    def __getattr__ (self, name) :
        try :
            return self._kw [name]
        except KeyError :
            raise AttributeError (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        return self._kw [key]
    # end def __getitem__

    def __getstate__ (self) :
        return self._kw
    # end def __getstate__

    def __iter__ (self) :
        return iter (self._kw)
    # end def __iter__

    def __len__ (self) :
        return len (self._kw)
    # end def __len__

    def __nonzero__ (self) :
        return bool (self._kw)
    # end def __nonzero__

    def __repr__ (self) :
        return "%s (%s)" % \
            (self.__class__.__name__, self._formatted_kw ())
    # end def __repr__

    def __setattr__ (self, name, value) :
        if name in self._properties :
            self.__super.__setattr__ (name, value)
        else :
            self._kw [name] = value
    # end def __setattr__

    def __setitem__ (self, name, value) :
        if name in self._properties :
            self.__super.__setattr__ (name, value)
        else :
            self._kw [name] = value
    # end def __setitem__

    def __setstate__ (self, state) :
        self.__dict__ ["_kw"] = state
    # end def __setstate__

    def __str__ (self) :
        return "(%s)" % (self._formatted_kw (), )
    # end def __str__

# end class Record

class Record_S (Record) :
    """Record usable as dict for %-interpolation with nested attributes.

       >>> c = Record_S (x = 1)
           >>> o = Record_S (a = 42, b = Record_S (a = 137, b = "foo", c = c))
       >>> "o.a = %(a)s, o.b.a = %(b.a)s, o.b.c.x = %(b.c.x)s" % o
       'o.a = 42, o.b.a = 137, o.b.c.x = 1'
    """

    def __getitem__ (self, key) :
        try :
            return self.__super.__getitem__ (key)
        except KeyError :
            o = self
            for k in key.split (".") :
                try :
                    o = getattr (o, k)
                except AttributeError :
                    raise KeyError (key)
            return o
    # end def __getitem__

# end class Record_S

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Record
