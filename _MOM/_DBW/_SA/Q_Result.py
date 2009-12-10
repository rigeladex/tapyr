# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM:DBW:SA.Q_Result
#
# Purpose
#    Provide the Q_Result interface using filter/order/... functions of
#    sqlalchemy
#
# Revision Dates
#     1-Dec-2009 (MG) Creation
#    10-Dec-2009 (MG) Adopted to new `TFL.Q_Exp`
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
>>> sa_table   = Table \\
...    ( "table", metadata
...    , Column ("id", Integer, primary_key = True)
...    , Column ("no", Integer)
...    )
...
>>> class Table (object) :
...     def __init__ (self, no) : self.no = no
...     def __str__  (self)     : return str (self.no)
...     __repr__ = __str__
...
>>> metadata.create_all (engine)
>>> _ = mapper (Table, sa_table)
>>> session.add_all (Table (x) for x in xrange (10))
>>> session.commit ()
>>> Q        = TFL.Attr_Query ()
>>> sa_query = session.query (Table)
>>> qr = Q_Result (Table, sa_query)
>>> qr.all ()
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> qr.count ()
10
>>> qr.order_by (Table.no % 2).all ()
[0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
>>> qs = qr.filter ((Table.no % 2) == 0)
>>> qs.count ()
5
>>> qs.all ()
[0, 2, 4, 6, 8]
>>> qt = qs.filter ((Table.no % 3) == 0)
>>> qt.count ()
2
>>> qt.all ()
[0, 6]
>>> qt.first ()
0
>>> qt.one ()
Traceback (most recent call last):
  ...
IndexError: Query result contains 2 entries
>>> qu = qt.filter (no = 0)
>>> qu.all ()
[0]
>>> qu = qt.filter (Table.no == 0)
>>> qu.one ()
0
>>> qv = qt.offset (1)
>>> qv.all ()
[6]
>>> qv.one ()
6
>>> qr.filter (Q.no == 2).all ()
[2]
>>> qr.filter (Q.no > 2).all ()
[3, 4, 5, 6, 7, 8, 9]
>>> qr.filter (Q.no >= 2).all ()
[2, 3, 4, 5, 6, 7, 8, 9]
>>> qr.filter (Q.no >= 2, Q.no <= 6).all ()
[2, 3, 4, 5, 6]
>>> qr.filter ((Q.no % 2) == 1).all ()
[1, 3, 5, 7, 9]
>>> qr.filter (((Q.no % 2) == 0) & ((Q.no % 4) == 0)).all ()
[0, 4, 8]
>>> qr.filter (((Q.no % 2) == 0) | ((Q.no % 3) == 0)).all ()
[0, 2, 3, 4, 6, 8, 9]

"""

from   _TFL                 import TFL
from   _MOM                 import MOM
import _TFL._Meta.Object
import _MOM._DBW._SA.Filter
import _MOM._DBW._SA.Sorted_By
from    sqlalchemy.orm      import exc as orm_exc
from    sqlalchemy.sql      import expression

class Q_Result (TFL.Meta.Object) :
    """Q_Result using SA-query funtion for the operations"""

    def __init__ (self, e_type, sa_query) :
        self.e_type   = e_type
        self.sa_query = sa_query
    # end def __init__

    def distinct (self) :
        return self.__class__ \
            (self.e_type, self.sa_query.distinct ())
    # end def distinct

    def filter (self, * criteria, ** eq_kw) :
        sa_criteria = []
        for c in criteria :
            if not isinstance (c, expression.Operators) :
                sa_criteria.append (c._sa_filter (self.e_type))
            else :
                sa_criteria.append (c)
        for attr, value in eq_kw.iteritems () :
            if attr == "type_name" :
                attr = "Type_Name"
            sa_criteria.append (getattr (self.e_type, attr) == value)
        if len (sa_criteria) > 1 :
            sa_criteria = (expression.and_ (* sa_criteria), )
        return self.__class__ \
            (self.e_type, self.sa_query.filter (* sa_criteria))
    # end def filter

    def limit (self, limit) :
        return self.__class__ \
            (self.e_type, self.sa_query.limit (limit))
    # end def limit

    def offset (self, offset) :
        return self.__class__ \
            (self.e_type, self.sa_query.offset (offset))
    # end def offset

    def one (self) :
        try :
            return self.sa_query.one ()
        except (orm_exc.MultipleResultsFound, orm_exc.NoResultFound) as exc :
            raise IndexError \
                ("Query result contains %s entries" % self.sa_query.count ())
    # end def one

    def order_by (self, criterion) :
        if not isinstance (criterion, expression.Operators) :
            joins, order_clause = criterion._sa_order_by (self.e_type)
        else :
            joins               = ()
            order_clause        = (criterion, )
        sa_query = self.sa_query.join (* joins).order_by (* order_clause)
        return self.__class__ (self.e_type, sa_query)
    # end def order_by

    def __getattr__ (self, name) :
        return getattr (self.sa_query, name)
    # end def __getattr__

    def __iter__ (self) :
        return iter (self.sa_query)
    # end def __iter__

# end class Q_Result

if __name__ != "__main__" :
    MOM.DBW.SA._Export ("*")
### __END__ MOM:DBW:SA.Q_Result
