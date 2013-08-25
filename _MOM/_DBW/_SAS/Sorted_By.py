# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SAS.Sorted_By
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
#    19-Mar-2010 (MG) `_sa_resolve_attribute` fixed
#     3-May-2010 (MG) Support for joins for order_by added
#     5-May-2010 (MG) Bug fixing
#     7-May-2010 (MG) Join handling changed (is now a list instead of a set
#                     to keep join order)
#     7-May-2010 (MG) `_sa_order_by` for TFL.Q_Exp.* fixed to support query
#                     attributes as well
#    12-May-2010 (MG) `Attr_Map` cleared
#    13-Sep-2011 (CT) All Q_Exp internal classes renamed to `_«name»_`
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
def _sa_order_by (self, SAQ, joins = None, order_clause = None, desc = False) :
    key = (self, SAQ)
    if key not in self._sa_cache :
        if joins        is None :
            joins        = []
        if order_clause is None :
            order_clause = []
        for c in self.criteria :
            if hasattr (c, "_sa_order_by") :
                c._sa_order_by (SAQ, joins, order_clause, desc)
            elif hasattr (c, "__call__") :
                raise NotImplementedError \
                    ( "Please implement _sa_order_by for custom "
                      "sorted by objects %s: %r" % (c.__class__, c)
                    )
            else :
                self._sa_resolve_attribute (SAQ, c, joins, order_clause, desc)
        self._sa_cache [key] = joins, order_clause
    return self._sa_cache [key]
# end def _sa_order_by

Attr_Map = {}

@TFL.Add_Method (TFL.Sorted_By)
def _sa_resolve_attribute (self, SAQ, c, joins, order_clause, desc = False) :
    if c.startswith ("-") :
        desc  = True
        c     = c [1:]
    parts     = c.split (".", 1)
    attr_name = parts [0]
    if len (parts) > 1 :
        _sa_filter = SAQ._ID_ENTITY_ATTRS.get (attr_name, None)
        if _sa_filter :
            aj, ac = _sa_filter (c, desc)
            joins.extend        (aj)
            order_clause.extend (ac)
        else :
            e_type = getattr      (SAQ, attr_name)
            self._sa_resolve_attribute \
                (e_type, parts [1], joins, order_clause, desc)
    else :
        attr_name = Attr_Map.get (attr_name, attr_name)
        column    = getattr (SAQ, attr_name)
        if isinstance (column, (list, tuple)) :
            joins.extend (column [0])
            column = column [1] [0]
        if desc :
            column = column.desc ()
        order_clause.append      (column)
# end def _sa_resolve_attribute

@TFL.Add_To_Class ( "_sa_order_by"
                  , TFL.Q_Exp._Bin_Bool_, TFL.Q_Exp._Bin_Expr_, TFL.Q_Exp._Get_
                  )
def _sa_order_by (self, SAQ, joins = None, order_clause = None, desc = False) :
    jo, oc = self._sa_filter (SAQ)
    if desc :
        oc = [c.desc () for c in oc ]
    if order_clause is None :
        return jo, oc
    joins.extend        (jo)
    order_clause.extend (oc)
# end def _sa_order_by

### __END__ MOM.DBW.SAS.Sorted_By
