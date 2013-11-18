# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.SQ
#
# Purpose
#    Structured query expressions for MOM meta object model
#
# Revision Dates
#    10-Jul-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

from   _TFL.I18N             import _, _T

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.Decorator

from   _MOM._Attr.Filter     import Q

@pyk.adapt__str__
class _SQ_ (TFL.Meta.Object) :
    """Structured query start point"""

    _Table = {}

    def __getitem__ (self, key) :
        try :
            result = self._Table [key]
        except KeyError :
            result = self._Table [key] = self._E_Type_ (key)
        return result
    # end def __getitem__

    def __str__ (self) :
        return "SQ"
    # end def __str__

# end class _SQ_

@TFL.Add_New_Method (_SQ_)
@pyk.adapt__str__
class _E_Type_ (TFL.Meta.Object) :
    """Structured query expression for a specific E_Type"""

    _attr      = None
    _attrs     = ()
    _distinct  = None
    _filters   = ()
    _group_by  = ()
    _kw        = {}
    _limit     = None
    _offset    = None
    _order_by  = ()
    _strict    = False

    def __init__ (self, t) :
        self.type_name = getattr (t, "type_name", t)
    # end def __init__

    def __call__ (self, q) :
        """Apply query expression to `q`."""
        if isinstance (q, MOM.Scope) :
            q = q [self.type_name]
        if isinstance (q, MOM.E_Type_Manager.Entity) :
            result = q.query (strict = self._strict)
        else :
            result = q
        if self._filters or self._kw :
            result = result.filter   (* self._filters, ** self._kw)
        if self._group_by :
            result = result.group_by (* self._group_by)
        if self._distinct is not None :
            result = result.distinct (self._distinct)
        for c in self._order_by :
            result = result.order_by (c)
        if self._limit is not None :
            result = result.limit    (self._limit)
        if self._offset is not None :
            result = result.offset   (self._offset)
        if self._attr is not None :
            result = result.attr     (self._attr)
        if self._attrs :
            result = result.attrs    (self._attrs)
        return result
    # end def __call__

    def apply (self, q) :
        """Apply query expression to `q`."""
        return self (q)
    # end def apply

    def attr (self, getter) :
        return self._clone (_attr = getter)
    # end def attr

    def attrs (self, * getters) :
        return self._clone (_attrs = getters)
    # end def attrs

    def distinct (self, value = True) :
        return self._clone (_distinct = value)
    # end def distinct

    def filter (self, * criteria, ** kw) :
        self._strict = kw.pop ("strict", False)
        sk           = kw.pop ("sort_key", ())
        return self._clone \
            ( _filters  = self._filters + criteria
            , _kw       = dict (self._kw, ** kw)
            , _order_by = self._order_by + ((sk, ) if sk else ())
            )
    # end def filter

    def group_by (self, * columns) :
        return self._clone (_group_by = self._group_by + columns)
    # end def group_by

    def limit (self, limit) :
        return self._clone (_limit = limit)
    # end def limit

    def offset (self, offset) :
        return self._clone (_offset = offset)
    # end def offset

    def order_by (self, * criteria) :
        return self._clone (_order_by = self._order_by + criteria)
    # end def order_by

    def _clone (self, ** kw) :
        cls    = self.__class__
        result = cls.__new__   (cls)
        result.__dict__.update (self.__dict__, ** kw)
        return result
    # end def _clone

    def __str__ (self) :
        result = ["SQ [%s]" % (self.type_name)]
        if self._filters or self._kw :
            args = list (str (f) for f in self._filters)
            args.extend \
                (   "%s = %r" % (k, v)
                for k, v in sorted (pyk.iteritems (self._kw))
                )
            result.append ("filter (%s)" % ", ".join (args))
        if self._group_by :
            args = list (str (f) for f in self._group_by)
            result.append ("group_by (%s)" % ", ".join (args))
        if self._distinct is not None :
            result.append ("distinct (%s)" % self._distinct)
        if self._order_by :
            args = list (str (f) for f in self._order_by)
            result.append ("order_by (%s)" % ", ".join (args))
        if self._limit is not None :
            result.append ("limit (%s)" % (self._limit, ))
        if self._offset is not None :
            result.append ("limit (%s)" % (self._offset, ))
        if self._attr is not None :
            result.append ("attr (%s)" % (self._attr, ))
        if self._attrs :
            result.append ("attrs (%s)" % (self._attrs, ))
        sep = "\n    ." if len (result) > 2 else "."
        return sep.join (result)
    # end def __str__

# end class _E_Type_

SQ = _SQ_ ()

__doc__ = """
    >>> sq = SQ ["PAP.Person"]
    >>> print (sq)
    SQ [PAP.Person]

    >>> print (sq.order_by (- Q.last_name))
    SQ [PAP.Person].order_by (- Q.last_name)

    >>> print (sq.order_by (- Q.last_name).limit (5).offset (10))
    SQ [PAP.Person]
        .order_by (- Q.last_name)
        .limit (5)
        .limit (10)

    >>> print (sq.filter (Q.last_name.STARTSWITH ("tanzer")))
    SQ [PAP.Person].filter (Q.last_name.startswith ('tanzer',))

    >>> print (sq)
    SQ [PAP.Person]

    >>> SQ ["PAP.Person"] is sq
    True

    >>> SQ ["PAP.Person_has_Phone"] is sq
    False

"""

if __name__ != "__main__" :
    MOM._Export ("SQ")
### __END__ MOM.SQ
