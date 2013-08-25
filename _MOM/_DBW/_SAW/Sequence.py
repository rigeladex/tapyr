# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.
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
#    MOM.DBW.SAW.Sequence
#
# Purpose
#    Wrap or emulate a database sequence
#
# Revision Dates
#    24-Jun-2013 (CT) Creation
#     8-Jul-2013 (CT) Change signature of `Sequence` to `attr`, not `attr_name`
#     8-Jul-2013 (CT) Use `.ATW.SA_Type.sized_int_type`, not `SA.types.Integer`
#    17-Jul-2013 (CT) Add argument `session` to methods needing that
#    26-Jul-2013 (CT) Add guard to `reserve`
#    26-Jul-2013 (CT) Factor `_reserve` to improve redefinability by descendents
#    28-Jul-2013 (CT) Change `seq_name` to lower case, remove `.`
#    31-Jul-2013 (CT) Use `scalar`, not `fetchone`, to extract col
#    31-Jul-2013 (CT) Use `session.con_man_seq`
#    31-Jul-2013 (CT) Change `reserve` to act only on `value > max_value`
#     1-Aug-2013 (CT) Update `session.seq_high`
#    ««revision-date»»···
#--

from   __future__     import division, print_function
from   __future__     import absolute_import, unicode_literals

from   _MOM           import MOM
from   _TFL           import TFL

from   _TFL.pyk       import pyk

from   _MOM._DBW._SAW import SA

import _MOM._DBW
import _MOM._DBW._SAW.DBS
import _MOM._DBW._SAW.SA_Type

import _TFL._Meta.Object

class _SAW_Sequence_ (TFL.Meta.Object) :
    """Wrap or emulate a database sequence"""

    _real_name          = "Sequence"

    _column_kw          = {}
    _table_kw           = {}

    def __init__ (self, attr, e_type) :
        self.e_type     = e_type
        self.ATW        = e_type.app_type._SAW
        self.DBW        = DBW   = e_type.app_type.DBW
        self.PNS        = PNS   = DBW.PNS
        self.dbs        = PNS.DBS
        self.attr       = attr
        self.name       = attr.name
        self.type_name  = e_type.type_name
        self.seq_name   = sn    = \
            ("%s_%s_seq" % (e_type._saw_table_name (DBW), attr.name))
        self.table_name = tn    = "%s_table"  % (sn, )
        self.sa_column  = col   = self._define_column (attr, DBW)
        self.sa_table   = table = self._define_table  (tn,   DBW, col)
        self.delete     = table.delete ().where (col < SA.sql.bindparam ("max"))
        self.insert     = table.insert ()
        self.select     = SA.sql.select([col]).limit (1).order_by (col.desc ())
    # end def __init__

    def commit (self, session) :
        session.con_man_seq.commit ()
    # end def commit

    def close (self, session) :
        self.rollback (session)
    # end def close

    def max_value (self, session) :
        conn    = session.con_man_seq.connection
        return conn.execute (self.select).scalar () or 0
    # end def max_value

    def next_value (self, session, commit = True) :
        con_man = session.con_man_seq
        conn    = con_man.connection
        sar     = conn.execute (self.insert.values ())
        result  = session.seq_high [self] = int (sar.inserted_primary_key [0])
        conn.execute (self.delete, max = result)
        if commit :
            con_man.commit ()
        return result
    # end def next_value

    def reserve (self, session, value, commit = True) :
        conn      = session.con_man_seq.connection
        max_value = self.max_value (session)
        ### `undo` of changes comes here with existing values, ignore those
        if value > max_value :
            self._reserve (conn, value)
            session.seq_high [self] = value
            if commit :
                session.con_man_seq.commit ()
        return value
    # end def reserve

    def rollback (self, session) :
        session.con_man_seq.rollback ()
    # end def rollback

    def _define_column (self, attr, DBW, * args, ** kw) :
        return SA.schema.Column \
            ( attr.name
            , self.ATW.SA_Type.sized_int_type (attr.Pickled_Type)
            , * args
            , ** dict (self._column_kw, primary_key = True, ** kw)
            )
    # end def _define_column

    def _define_table (self, tn, DBW, * cols, ** kw) :
        return SA.schema.Table \
            ( tn, self.ATW.metadata, * cols
            , ** dict (self._table_kw, ** kw)
            )
    # end def _define_table

    def _reserve (self, conn, value) :
        conn.execute (self.insert.values (** {self.attr.name : value}))
        conn.execute (self.delete, max = value)
    # end def _reserve

    def __repr__ (self) :
        attr = self.attr
        return "<Sequence for %s attribute %s.%s>" % \
            (attr.typ, self.type_name, attr.name)
    # end def __repr__

Sequence = _SAW_Sequence_ # end class

class _SAW_Sequence_S_ (Sequence) :
    """Wrap a database sequence for a RDBMS supporting sequences"""

    _seq_kw             = {}

    def __init__ (self, attr, type_name, ** kw) :
        self._seq_kw = kw
        self.__super.__init__ (attr, type_name)
    # end def __init__

    def _define_column (self, name, DBW, * args, ** kw) :
        self.sa_seq = seq = SA.schema.Sequence (self.seq_name, ** self._seq_kw)
        return self.__super._define_column     (name, DBW, seq, * args, ** kw)
    # end def _define_column

# end class _SAW_Sequence_S_

if __name__ != "__main__" :
    MOM.DBW.SAW._Export ("*", "_SAW_Sequence_S_")
### __END__ MOM.DBW.SAW.Sequence
