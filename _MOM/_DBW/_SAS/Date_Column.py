# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBQ.SAS.Date_Column.
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
#    MOM.DBW.SAS.Date_Column
#
# Purpose
#    A special column which supports more features for date queries.
#
# Revision Dates
#    25-Jul-2011 (MG) Creation
#    ««revision-date»»···
#--

from    __future__     import unicode_literals
from    sqlalchemy     import types, schema
from    sqlalchemy.sql import extract, expression
from   _MOM            import MOM
import _MOM._DBW._SAS

def _operator_ (func) :
    def _ (self, rhs) :
        return self.Operator (self, func.__name__, rhs)
    # end def _
    _.__name__ = func.__name__
    return _
# end def _operator_

class Date_Compare (object) :
    """Intermediate class handling the special date queries."""

    class Operator (object) :
        """Handling of the real comparison"""

        ### for sqlite we need to fallback to the strftime function
        strftime_map   = dict \
            ( year     = "Y"
            , month    = "m"
            , day      = "d"
            , dayofweek= "w"
            )

        ### unfortunately, the textclause we generate for sqlie does not
        ### support any operators
        operator_map   = dict \
            ( __eq__   = "=="
            , __ne__   = "!="
            , __le__   = "<="
            , __lt__   = "<"
            , __ge__   = ">="
            , __gt__   = ">"
            )

        def __init__ (self, compare, operator, rhs) :
            self.compare  = compare
            self.operator = operator
            self.table    = compare.table
            self.rhs      = rhs
        # end def __init__

        def __clause_element__ (self) :
            return self
        # end def __clause_element__

        @property
        def _from_objects (self) :
            return ()
        # end def _from_objects

        @property
        def _hide_froms (self) :
            return ()
        # end def _hide_froms

        def _compiler_dispatch (self, compiler, ** kw) :
            col = self.compare.column
            if compiler.dialect.name == "sqlite" :
                expr = expression.text \
                    ( "CAST(strftime ('%%%s', %s) AS INTEGER) %s %d"
                    % ( self.strftime_map [self.compare.what]
                      , col
                      , self.operator_map [self.operator]
                      , self.rhs
                      )
                    )
            else :
                expr = getattr \
                    (extract (self.compare.what, col), self.operator) (self.rhs)
            return expr._compiler_dispatch (compiler, ** kw)
        # end def _compiler_dispatch

    # end class Operator

    def __init__ (self, column, what) :
        self.table  = column.table
        self.column = column
        self.what   = what
    # end def __init__

    @_operator_
    def __eq__ (self, rhs) : pass

    @_operator_
    def __ne__ (self, rhs) : pass

    @_operator_
    def __le__ (self, rhs) : pass

    @_operator_
    def __ge__ (self, rhs) : pass

    @_operator_
    def __lt__ (self, rhs) : pass

    @_operator_
    def __gt__ (self, rhs) : pass

# end class Date_Compare

def _compare_ (func) :
    def _ (self) :
        return Date_Compare (self, func.__name__)
    # end def _
    _.__name__ = func.__name__
    return property (_)
# end def _compare_

class Date_Column (schema.Column) :
    """Special column which addes compare functions which map to the extract
       function of sqlalchemy.
    """

    @_compare_
    def year (self) : pass

    @_compare_
    def month (self) : pass

# end class Date_Column

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Date_Column
