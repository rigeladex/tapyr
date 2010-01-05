# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SA.Sorted_By
#
# Purpose
#    Monkey patch TFL.Sorted_By to add support for creating the
#    SQLAlchemy order_by clause
#
# Revision Dates
#    20-Sep-2009 (MG) Creation
#    14-Oct-2009 (CT) Signature of `Sorted_By` changed from `criteria`
#                     to `* criteria`
#    03-Dec-2009 (MG) `_sa_order_by` changed to support possibly needed joins
#                     as well (`_sa_resolve_attribute` added)
#    15-Dec-2009 (MG) `Attr_Map` added, added `table` to key for sort
#                     expression caching (to avoid reuse of the worng sorting
#                     cache)
#    18-Dec-2009 (MG) `_sa_order_by` for `TFL.Q_Exp.*` added
#    ««revision-date»»···
#--

"""
>>> from sqlalchemy     import create_engine
>>> from sqlalchemy     import Table, Column, Integer, String, Boolean, MetaData, ForeignKey
>>> from sqlalchemy.orm import mapper, sessionmaker, relation, synonym
>>> engine     = create_engine ('sqlite:///:memory:', echo = False)
>>> metadata   = MetaData      ()
>>> Session    = sessionmaker  (bind=engine)
>>> session    = Session       ()
>>> sa_table = Table \\
...    ( "table", metadata
...    , Column ("id", Integer, primary_key = True)
...    , Column ("a",  Integer)
...    , Column ("b",  Integer)
...    , Column ("c",  String (50))
...    )
...
>>> class Table (object) :
...     def __init__ (self, a, b ,c) :
...         self.a = a
...         self.b = b
...         self.c = c
...     # end def __init__
...     def __str__ (self) :
...         return "(a = %s, b = %s, c = %s)" % \\
...             (self.a, self.b, self.c)
...     # end def __str__
...
>>> metadata.create_all (engine)
>>> _ = mapper (Table, sa_table)
>>> session.add_all \\
...    ( ( Table (1, 1, "abcd")
...       , Table (1, 2, "ABCD")
...       , Table (1, 2, "efg")
...       , Table (2, 1, "xyz")
...       , Table (2, 1, " xyzz")
...       , Table (2, 1, "  xyzzz")
...       )
...     )
...
>>> session.commit ()
>>> def _show (table, sorted_by) :
...     joins, order_clause = sorted_by._sa_order_by (table)
...     query               = session.query (table).join (* joins)
...     print "\\n".join (str (s) for s in query.order_by (* order_clause))
... # end def _show
>>> Sorted_By = TFL.Sorted_By
>>> _show (Table, Sorted_By ( "a", "b"))
(a = 1, b = 1, c = abcd)
(a = 1, b = 2, c = ABCD)
(a = 1, b = 2, c = efg)
(a = 2, b = 1, c = xyz)
(a = 2, b = 1, c =  xyzz)
(a = 2, b = 1, c =   xyzzz)
>>> _show (Table, Sorted_By ( "a", "-b"))
(a = 1, b = 2, c = ABCD)
(a = 1, b = 2, c = efg)
(a = 1, b = 1, c = abcd)
(a = 2, b = 1, c = xyz)
(a = 2, b = 1, c =  xyzz)
(a = 2, b = 1, c =   xyzzz)
>>> _show (Table, Sorted_By ( "b",  "a"))
(a = 1, b = 1, c = abcd)
(a = 2, b = 1, c = xyz)
(a = 2, b = 1, c =  xyzz)
(a = 2, b = 1, c =   xyzzz)
(a = 1, b = 2, c = ABCD)
(a = 1, b = 2, c = efg)
>>> _show (Table, Sorted_By ("-b",  "a"))
(a = 1, b = 2, c = ABCD)
(a = 1, b = 2, c = efg)
(a = 1, b = 1, c = abcd)
(a = 2, b = 1, c = xyz)
(a = 2, b = 1, c =  xyzz)
(a = 2, b = 1, c =   xyzzz)
>>> _show (Table, Sorted_By ("-b", "-a"))
(a = 1, b = 2, c = ABCD)
(a = 1, b = 2, c = efg)
(a = 2, b = 1, c = xyz)
(a = 2, b = 1, c =  xyzz)
(a = 2, b = 1, c =   xyzzz)
(a = 1, b = 1, c = abcd)
>>> _show (Table, Sorted_By ( "b",  "c"))
(a = 2, b = 1, c =   xyzzz)
(a = 2, b = 1, c =  xyzz)
(a = 1, b = 1, c = abcd)
(a = 2, b = 1, c = xyz)
(a = 1, b = 2, c = ABCD)
(a = 1, b = 2, c = efg)
>>> _show (Table, Sorted_By ( "b", "-c"))
(a = 2, b = 1, c = xyz)
(a = 1, b = 1, c = abcd)
(a = 2, b = 1, c =  xyzz)
(a = 2, b = 1, c =   xyzzz)
(a = 1, b = 2, c = efg)
(a = 1, b = 2, c = ABCD)
>>> _show (Table, Sorted_By ("-b",  "c"))
(a = 1, b = 2, c = ABCD)
(a = 1, b = 2, c = efg)
(a = 2, b = 1, c =   xyzzz)
(a = 2, b = 1, c =  xyzz)
(a = 1, b = 1, c = abcd)
(a = 2, b = 1, c = xyz)
>>> _show (Table, Sorted_By ("-b", "-c"))
(a = 1, b = 2, c = efg)
(a = 1, b = 2, c = ABCD)
(a = 2, b = 1, c = xyz)
(a = 1, b = 1, c = abcd)
(a = 2, b = 1, c =  xyzz)
(a = 2, b = 1, c =   xyzzz)
>>> _show (Table, Sorted_By ("c"))
(a = 2, b = 1, c =   xyzzz)
(a = 2, b = 1, c =  xyzz)
(a = 1, b = 2, c = ABCD)
(a = 1, b = 1, c = abcd)
(a = 1, b = 2, c = efg)
(a = 2, b = 1, c = xyz)
"""

from   _TFL                 import TFL
import _TFL.Decorator
import _TFL.Sorted_By
import _TFL.Q_Exp

TFL.Sorted_By._sa_cache = {}

@TFL.Add_Method (TFL.Sorted_By)
def _sa_order_by (self, table, joins = None, order_clause = None) :
    key = (self, table)
    if self not in self._sa_cache :
        if joins        is None :
            joins        = set ()
        if order_clause is None :
            order_clause = []
        for c in self.criteria :
            if hasattr (c, "_sa_order_by") :
                c._sa_order_by (table, joins, order_clause)
            elif hasattr (c, "__call__") :
                raise NotImplementedError \
                    ( "Please implement _sa_order_by for custom "
                      "sorted by objects %s: %r" % (c.__class__, c)
                    )
            else :
                assert c.count (".") < 2, "Check if we can support more levels"
                self._sa_resolve_attribute (table, c, joins, order_clause)
        self._sa_cache [key] = joins, order_clause
    return self._sa_cache [key]
# end def _sa_order_by

Attr_Map = { "pid" : "id", "-pid" : "-id"}

@TFL.Add_Method (TFL.Sorted_By)
def _sa_resolve_attribute (self, table, c, joins, order_clause) :
    parts     = c.split (".", 1)
    attr_name = parts [0]
    if len (parts) > 1 :
        e_type = getattr           (table, attr_name).Class
        joins.add                  (e_type)
        self._sa_resolve_attribute (e_type, parts [1], joins, order_clause)
    else :
        attr_name = Attr_Map.get (attr_name, attr_name)
        if attr_name.startswith ("-") :
            order_clause.append (getattr (table, attr_name [1:]).desc ())
        else :
            order_clause.append (getattr (table, attr_name))
# end def _sa_resolve_attribute

@TFL.Add_To_Class ( "_sa_order_by"
                  , TFL.Q_Exp.Bin_Bool, TFL.Q_Exp.Bin_Expr, TFL.Q_Exp.Get
                  )
def _sa_order_by (self, table, joins = None, order_clause = None) :
    if order_clause is None :
        return (), (self._sa_filter (table), )
    order_clause.append (self._sa_filter (table))
# end def _sa_order_by

### __END__ MOM.DBW.SA.Sorted_By
