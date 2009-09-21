# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
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
#    MOM.DBW.SA.Sorted_By
#
# Purpose
#    Monkey patch TFL.Sorted_By to add support for creating the
#    SQLAlchemy order_by clause
#
# Revision Dates
#    20-Sep-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM._DBW._SA        import SA
from   _TFL                 import TFL
import _TFL.Sorted_By

def _sa_order_by (self, table) :
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
    ...     print "\\n".join (str (s) for s in session.query (table).order_by \\
    ...         (* sorted_by._sa_order_by (table)))
    ... # end def _show
    >>> Sorted_By = TFL.Sorted_By
    >>> _show (Table, Sorted_By ([ "a", "b"]))
    (a = 1, b = 1, c = abcd)
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 2, c = efg)
    (a = 2, b = 1, c = xyz)
    (a = 2, b = 1, c =  xyzz)
    (a = 2, b = 1, c =   xyzzz)
    >>> _show (Table, Sorted_By ([ "a", "-b"]))
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 2, c = efg)
    (a = 1, b = 1, c = abcd)
    (a = 2, b = 1, c = xyz)
    (a = 2, b = 1, c =  xyzz)
    (a = 2, b = 1, c =   xyzzz)
    >>> _show (Table, Sorted_By ([ "b",  "a"]))
    (a = 1, b = 1, c = abcd)
    (a = 2, b = 1, c = xyz)
    (a = 2, b = 1, c =  xyzz)
    (a = 2, b = 1, c =   xyzzz)
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 2, c = efg)
    >>> _show (Table, Sorted_By (["-b",  "a"]))
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 2, c = efg)
    (a = 1, b = 1, c = abcd)
    (a = 2, b = 1, c = xyz)
    (a = 2, b = 1, c =  xyzz)
    (a = 2, b = 1, c =   xyzzz)
    >>> _show (Table, Sorted_By (["-b", "-a"]))
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 2, c = efg)
    (a = 2, b = 1, c = xyz)
    (a = 2, b = 1, c =  xyzz)
    (a = 2, b = 1, c =   xyzzz)
    (a = 1, b = 1, c = abcd)
    >>> _show (Table, Sorted_By ([ "b",  "c"]))
    (a = 2, b = 1, c =   xyzzz)
    (a = 2, b = 1, c =  xyzz)
    (a = 1, b = 1, c = abcd)
    (a = 2, b = 1, c = xyz)
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 2, c = efg)
    >>> _show (Table, Sorted_By ([ "b", "-c"]))
    (a = 2, b = 1, c = xyz)
    (a = 1, b = 1, c = abcd)
    (a = 2, b = 1, c =  xyzz)
    (a = 2, b = 1, c =   xyzzz)
    (a = 1, b = 2, c = efg)
    (a = 1, b = 2, c = ABCD)
    >>> _show (Table, Sorted_By (["-b",  "c"]))
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 2, c = efg)
    (a = 2, b = 1, c =   xyzzz)
    (a = 2, b = 1, c =  xyzz)
    (a = 1, b = 1, c = abcd)
    (a = 2, b = 1, c = xyz)
    >>> _show (Table, Sorted_By (["-b", "-c"]))
    (a = 1, b = 2, c = efg)
    (a = 1, b = 2, c = ABCD)
    (a = 2, b = 1, c = xyz)
    (a = 1, b = 1, c = abcd)
    (a = 2, b = 1, c =  xyzz)
    (a = 2, b = 1, c =   xyzzz)
    >>> _show (Table, Sorted_By (["c"]))
    (a = 2, b = 1, c =   xyzzz)
    (a = 2, b = 1, c =  xyzz)
    (a = 1, b = 2, c = ABCD)
    (a = 1, b = 1, c = abcd)
    (a = 1, b = 2, c = efg)
    (a = 2, b = 1, c = xyz)
    """
    result = []
    for c in self.criteria :
        if hasattr (c, "_sa_order_by") :
            result.extend (c._sa_order_by (table))
        elif hasattr (c, "__call__") :
            raise NotImplementedError \
                ("Please implement _sa_order_by for custom sorted by objects")
        elif c.startswith ("-") :
            result.append (getattr (table, c [1:]).desc ())
        else :
            result.append (getattr (table, c))
    return result
# end def _sa_order_by
TFL.Sorted_By._sa_order_by = _sa_order_by

### __END__ MOM.DBW.SA.Sorted_By
